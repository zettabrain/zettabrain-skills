"""
FastAPI web application for ZettaBrain Skills
Multi-industry document generation with discovery document support
"""

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import os
import markdown
from typing import Optional, List, Dict, Any
from weasyprint import HTML, CSS
from io import BytesIO
from datetime import datetime, timedelta
import glob

from zettabrain_skills.skills.parser import load_skill
from zettabrain_skills.core.engine import GenerationEngine
from zettabrain_skills.core.models import GenerationRequest
from zettabrain_skills.discovery.parser import DiscoveryParser

# Initialize FastAPI app
app = FastAPI(
    title="ZettaBrain Skills - AI Document Generation",
    description="Generate professional business documents with industry-specific skills",
    version="0.5.0"
)

# Setup templates directory
BASE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Mount static files
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Store generated documents in memory (for demo)
generated_documents = []

# Load business context from discovery document (if exists)
BUSINESS_INFO = None
BUSINESS_CONTEXT = None
discovery_path = Path("examples/discovery-documents/3rva-discovery.md")

if discovery_path.exists():
    try:
        parser = DiscoveryParser()
        BUSINESS_INFO = parser.parse_document(discovery_path)
        BUSINESS_CONTEXT = BUSINESS_INFO.to_skill_context()
        print(f"✓ Loaded business context for {BUSINESS_INFO.company_name}")
    except Exception as e:
        print(f"Warning: Could not load discovery document: {e}")
        BUSINESS_INFO = None
        BUSINESS_CONTEXT = None


def load_available_skills() -> List[Dict[str, Any]]:
    """Load all available skill files from examples directory"""
    skills = []

    # Find all markdown files in examples/
    skill_files = glob.glob("examples/*.md")

    for skill_file in skill_files:
        try:
            skill = load_skill(skill_file)
            skills.append({
                "file": skill_file,
                "name": skill.name.replace("-", " ").title(),
                "description": skill.description,
                "business_type": skill.business_type,
                "version": skill.version
            })
        except Exception as e:
            print(f"Warning: Could not load skill {skill_file}: {e}")
            continue

    return sorted(skills, key=lambda x: x["name"])


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with multi-industry skill selection"""
    skills = load_available_skills()

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "skills": skills,
            "business_context": BUSINESS_CONTEXT is not None,
            "business_name": BUSINESS_INFO.company_name if BUSINESS_INFO else None
        }
    )


@app.get("/3rva", response_class=HTMLResponse)
async def legacy_3rva_home(request: Request):
    """Legacy 3RVA-specific page for backwards compatibility"""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"title": "3RVA Quote Generator"}
    )


@app.post("/generate", response_class=HTMLResponse)
async def legacy_generate_quote(
    request: Request,
    customer_request: str = Form(...),
    customer_name: str = Form(""),
    customer_email: str = Form(""),
    customer_phone: str = Form("")
):
    """Legacy 3RVA quote generation endpoint for backwards compatibility"""

    try:
        # Find the 3RVA skill file
        skill_path = Path("examples/3rva-quote-full.md")
        if not skill_path.exists():
            skill_path = Path.cwd() / "examples" / "3rva-quote-full.md"

        if not skill_path.exists():
            raise HTTPException(
                status_code=500,
                detail="Skill file not found. Please ensure examples/3rva-quote-full.md exists."
            )

        # Load skill
        skill = load_skill(str(skill_path))

        # Initialize engine
        engine = GenerationEngine()

        # Check if Ollama is running
        if not engine.llm_provider.check_health():
            return templates.TemplateResponse(
                request=request,
                name="error.html",
                context={
                    "error": "Ollama is not running. Please start Ollama first.",
                    "suggestion": "Run: ollama serve"
                }
            )

        # Get current date
        today = datetime.now()
        valid_until = today + timedelta(days=7)
        date_str = today.strftime("%B %d, %Y")
        valid_until_str = valid_until.strftime("%B %d, %Y")
        quote_date_code = today.strftime("%Y%m%d")

        # Build enhanced request with customer details, current date, and business context
        enhanced_parts = []

        # Add business context if available
        if BUSINESS_CONTEXT:
            enhanced_parts.append(BUSINESS_CONTEXT)
            enhanced_parts.append("\n---\n")

        # Add date information
        enhanced_parts.append(f"""TODAY'S DATE: {date_str}
VALID UNTIL DATE: {valid_until_str}
QUOTE NUMBER FORMAT: 3RVA-{quote_date_code}-XXX (use random 3 digits for XXX)
""")

        # Add customer information
        if customer_name:
            enhanced_parts.append(f"Customer: {customer_name}\n")
        if customer_email:
            enhanced_parts.append(f"Email: {customer_email}\n")
        if customer_phone:
            enhanced_parts.append(f"Phone: {customer_phone}\n")

        # Add customer request
        enhanced_parts.append(f"\nCustomer Request:\n{customer_request}")

        enhanced_request = "".join(enhanced_parts)

        # Generate quote
        gen_request = GenerationRequest(
            input=enhanced_request,
            skill_name=skill.name,
            business_id="3rva"
        )

        result = engine.generate(skill, gen_request)

        if not result.success:
            return templates.TemplateResponse(
                request=request,
                name="error.html",
                context={
                    "error": f"Generation failed: {result.error}",
                    "suggestion": "Please try again or check Ollama logs."
                }
            )

        # Store quote
        quote_data = {
            "id": result.id,
            "skill_name": skill.name,
            "customer_name": customer_name or "Customer",
            "customer_email": customer_email,
            "customer_phone": customer_phone,
            "request": customer_request,
            "content": result.content,
            "created_at": result.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "generation_time": f"{result.generation_time_ms / 1000:.1f}s"
        }
        generated_documents.insert(0, quote_data)

        # Keep only last 50 documents
        if len(generated_documents) > 50:
            generated_documents.pop()

        return templates.TemplateResponse(
            request=request,
            name="quote.html",
            context={"quote": quote_data}
        )

    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={
                "error": str(e),
                "suggestion": "Please check that Ollama is running and the skill file exists."
            }
        )


@app.post("/generate-document", response_class=HTMLResponse)
async def generate_document(
    request: Request,
    skill_file: str = Form(...),
    input_text: str = Form(...),
    customer_name: str = Form(""),
    customer_email: str = Form(""),
    customer_phone: str = Form("")
):
    """Generate a document using selected skill"""

    try:
        # Load skill
        skill_path = Path(skill_file)
        if not skill_path.exists():
            raise HTTPException(
                status_code=400,
                detail=f"Skill file not found: {skill_file}"
            )

        skill = load_skill(str(skill_path))

        # Initialize engine
        engine = GenerationEngine()

        # Check if Ollama is running
        if not engine.llm_provider.check_health():
            return templates.TemplateResponse(
                request=request,
                name="error.html",
                context={
                    "error": "Ollama is not running. Please start Ollama first.",
                    "suggestion": "Run: ollama serve"
                }
            )

        # Get current date
        today = datetime.now()
        date_str = today.strftime("%B %d, %Y")

        # Build enhanced request
        enhanced_parts = []

        # Add business context if available and relevant
        if BUSINESS_CONTEXT and skill.business_type in ["sales", "hvac", "refrigerant"]:
            enhanced_parts.append(BUSINESS_CONTEXT)
            enhanced_parts.append("\n---\n")

        # Add date information
        enhanced_parts.append(f"TODAY'S DATE: {date_str}\n\n")

        # Add customer information
        if customer_name:
            enhanced_parts.append(f"Customer/Client: {customer_name}\n")
        if customer_email:
            enhanced_parts.append(f"Email: {customer_email}\n")
        if customer_phone:
            enhanced_parts.append(f"Phone: {customer_phone}\n")

        if customer_name or customer_email or customer_phone:
            enhanced_parts.append("\n")

        # Add main request
        enhanced_parts.append(input_text)

        enhanced_request = "".join(enhanced_parts)

        # Generate document
        gen_request = GenerationRequest(
            input=enhanced_request,
            skill_name=skill.name,
            business_id="default"
        )

        result = engine.generate(skill, gen_request)

        if not result.success:
            return templates.TemplateResponse(
                request=request,
                name="error.html",
                context={
                    "error": f"Generation failed: {result.error}",
                    "suggestion": "Please try again or check Ollama logs."
                }
            )

        # Store document
        doc_data = {
            "id": result.id,
            "skill_name": skill.name,
            "skill_display": skill.name.replace("-", " ").title(),
            "customer_name": customer_name or "Customer",
            "customer_email": customer_email,
            "customer_phone": customer_phone,
            "request": input_text,
            "content": result.content,
            "created_at": result.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "generation_time": f"{result.generation_time_ms / 1000:.1f}s"
        }
        generated_documents.insert(0, doc_data)

        # Keep only last 50 documents
        if len(generated_documents) > 50:
            generated_documents.pop()

        return templates.TemplateResponse(
            request=request,
            name="document.html",
            context={"document": doc_data}
        )

    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={
                "error": str(e),
                "suggestion": "Please check that Ollama is running and the skill file exists."
            }
        )


@app.get("/generated", response_class=HTMLResponse)
async def list_generated(request: Request):
    """List all generated documents"""
    return templates.TemplateResponse(
        request=request,
        name="generated.html",
        context={"documents": generated_documents}
    )


@app.get("/quotes", response_class=HTMLResponse)
async def legacy_list_quotes(request: Request):
    """Legacy endpoint - redirect to /generated"""
    return RedirectResponse(url="/generated")


@app.get("/document/{doc_id}", response_class=HTMLResponse)
async def view_document(request: Request, doc_id: str):
    """View a specific document"""
    document = next((d for d in generated_documents if d["id"] == doc_id), None)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    return templates.TemplateResponse(
        request=request,
        name="document.html",
        context={"document": document}
    )


@app.get("/quote/{quote_id}", response_class=HTMLResponse)
async def legacy_view_quote(request: Request, quote_id: str):
    """Legacy endpoint - redirect to /document"""
    return RedirectResponse(url=f"/document/{quote_id}")


@app.get("/document/{doc_id}/pdf")
async def download_document_pdf(doc_id: str):
    """Download document as PDF"""
    document = next((d for d in generated_documents if d["id"] == doc_id), None)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Convert markdown to HTML
    md = markdown.Markdown(extensions=['extra', 'nl2br'])
    content_html = md.convert(document['content'])

    # Create PDF HTML template
    pdf_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{
                size: letter;
                margin: 0.75in;
            }}
            body {{
                font-family: Arial, sans-serif;
                font-size: 11pt;
                line-height: 1.6;
                color: #333;
            }}
            .header {{
                text-align: center;
                margin-bottom: 30px;
                border-bottom: 3px solid #5b64f4;
                padding-bottom: 20px;
            }}
            .header h1 {{
                color: #5b64f4;
                font-size: 24pt;
                margin: 0 0 10px 0;
            }}
            .header p {{
                color: #666;
                margin: 5px 0;
            }}
            .meta {{
                background: #f8f9ff;
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 25px;
                border-left: 4px solid #5b64f4;
            }}
            .meta-item {{
                margin: 5px 0;
            }}
            .meta-label {{
                font-weight: bold;
                color: #5b64f4;
            }}
            .content {{
                white-space: pre-wrap;
                font-family: 'Courier New', monospace;
                background: #fafafa;
                padding: 20px;
                border: 1px solid #e0e0e0;
                border-radius: 5px;
            }}
            .footer {{
                margin-top: 40px;
                padding-top: 20px;
                border-top: 2px solid #e0e0e0;
                text-align: center;
                color: #999;
                font-size: 9pt;
            }}
            h1, h2, h3 {{
                color: #5b64f4;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>ZettaBrain Skills</h1>
            <p>AI-Powered Professional Document Generation</p>
            <p>{document.get('skill_display', document.get('skill_name', 'Document'))}</p>
        </div>

        <div class="meta">
            <div class="meta-item">
                <span class="meta-label">Customer:</span> {document['customer_name']}
            </div>
            {'<div class="meta-item"><span class="meta-label">Email:</span> ' + document['customer_email'] + '</div>' if document.get('customer_email') else ''}
            {'<div class="meta-item"><span class="meta-label">Phone:</span> ' + document['customer_phone'] + '</div>' if document.get('customer_phone') else ''}
            <div class="meta-item">
                <span class="meta-label">Generated:</span> {document['created_at']}
            </div>
            <div class="meta-item">
                <span class="meta-label">Document ID:</span> {document['id']}
            </div>
        </div>

        <div class="content">
{document['content']}
        </div>

        <div class="footer">
            <p>Generated by ZettaBrain Skills | AI-Powered Document Generation Platform</p>
            <p>www.zettabrain.com</p>
        </div>
    </body>
    </html>
    """

    # Generate PDF
    pdf_bytes = BytesIO()
    HTML(string=pdf_html).write_pdf(pdf_bytes)
    pdf_bytes.seek(0)

    # Return PDF
    skill_name = document.get('skill_name', 'document').replace(' ', '-')
    return Response(
        content=pdf_bytes.read(),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=zettabrain-{skill_name}-{doc_id[:8]}.pdf"
        }
    )


@app.get("/quote/{quote_id}/pdf")
async def legacy_download_pdf(quote_id: str):
    """Legacy endpoint - redirect to /document/{id}/pdf"""
    return RedirectResponse(url=f"/document/{quote_id}/pdf")


@app.get("/discovery", response_class=HTMLResponse)
async def view_discovery(request: Request):
    """View loaded business information"""
    return templates.TemplateResponse(
        request=request,
        name="discovery.html",
        context={"business_info": BUSINESS_INFO}
    )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    from zettabrain_skills.llm.providers.ollama import OllamaProvider

    provider = OllamaProvider()
    ollama_status = provider.check_health()

    return {
        "status": "healthy" if ollama_status else "degraded",
        "ollama": "running" if ollama_status else "not running",
        "business_context_loaded": BUSINESS_CONTEXT is not None,
        "business_name": BUSINESS_INFO.company_name if BUSINESS_INFO else None,
        "version": "0.5.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
