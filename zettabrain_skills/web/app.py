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
    version="1.0.0"
)

# Setup templates directory
BASE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Mount static files
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Store generated documents in memory (for demo)
generated_documents = []

# Load business context from discovery document (if configured)
BUSINESS_INFO = None
BUSINESS_CONTEXT = None
discovery_path_str = os.getenv("DISCOVERY_DOCUMENT")

if discovery_path_str:
    discovery_path = Path(discovery_path_str)
    if discovery_path.exists():
        try:
            parser = DiscoveryParser()
            BUSINESS_INFO = parser.parse_document(discovery_path)
            BUSINESS_CONTEXT = BUSINESS_INFO.to_skill_context()
            print(f"Loaded business context for {BUSINESS_INFO.company_name}")
        except Exception as e:
            print(f"Warning: Could not load discovery document: {e}")


SKILLS_DIR = os.getenv("SKILLS_DIR", "examples")


def load_available_skills() -> List[Dict[str, Any]]:
    """Load all available skill files from skills directory"""
    skills = []

    skill_files = glob.glob(f"{SKILLS_DIR}/*.md")

    for skill_file in skill_files:
        try:
            skill = load_skill(skill_file)
            display_name = skill.name.replace("-", " ").title()

            skills.append({
                "file": skill_file,
                "name": display_name,
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
    """Home page with skill selection"""
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
        skill_path = Path(skill_file)
        if not skill_path.exists():
            raise HTTPException(
                status_code=400,
                detail=f"Skill file not found: {skill_file}"
            )

        skill = load_skill(str(skill_path))

        engine = GenerationEngine()

        if not engine.llm_provider.check_health():
            return templates.TemplateResponse(
                request=request,
                name="error.html",
                context={
                    "error": "LLM provider is not running.",
                    "suggestion": "Run: ollama serve"
                }
            )

        today = datetime.now()
        date_str = today.strftime("%B %d, %Y")

        enhanced_parts = []

        if BUSINESS_CONTEXT:
            enhanced_parts.append(BUSINESS_CONTEXT)
            enhanced_parts.append("\n---\n")

        enhanced_parts.append(f"TODAY'S DATE: {date_str}\n\n")

        if customer_name:
            enhanced_parts.append(f"Customer/Client: {customer_name}\n")
        if customer_email:
            enhanced_parts.append(f"Email: {customer_email}\n")
        if customer_phone:
            enhanced_parts.append(f"Phone: {customer_phone}\n")

        if customer_name or customer_email or customer_phone:
            enhanced_parts.append("\n")

        enhanced_parts.append(input_text)
        enhanced_request = "".join(enhanced_parts)

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
                    "suggestion": "Please try again or check LLM provider logs."
                }
            )

        skill_display = skill.name.replace("-", " ").title()

        doc_data = {
            "id": result.id,
            "skill_name": skill.name,
            "skill_display": skill_display,
            "customer_name": customer_name or "Customer",
            "customer_email": customer_email,
            "customer_phone": customer_phone,
            "request": input_text,
            "content": result.content,
            "citations": result.citations,
            "created_at": result.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "generation_time": f"{result.generation_time_ms / 1000:.1f}s"
        }
        generated_documents.insert(0, doc_data)

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
                "suggestion": "Please check that the LLM provider is running and the skill file exists."
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


@app.get("/document/{doc_id}/pdf")
async def download_document_pdf(doc_id: str):
    """Download document as PDF"""
    document = next((d for d in generated_documents if d["id"] == doc_id), None)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    md = markdown.Markdown(extensions=['extra', 'nl2br'])
    content_html = md.convert(document['content'])

    company_name = BUSINESS_INFO.company_name if BUSINESS_INFO else "ZettaBrain Skills"

    pdf_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{ size: letter; margin: 0.75in; }}
            body {{ font-family: Arial, sans-serif; font-size: 11pt; line-height: 1.6; color: #333; }}
            .header {{ text-align: center; margin-bottom: 30px; border-bottom: 3px solid #667eea; padding-bottom: 20px; }}
            .header h1 {{ color: #667eea; font-size: 24pt; margin: 0 0 10px 0; font-weight: 700; }}
            .header .doc-type {{ color: #888; font-size: 11pt; font-style: italic; }}
            .meta {{ background: #f8f9ff; padding: 15px; border-radius: 5px; margin-bottom: 25px; border-left: 4px solid #667eea; }}
            .meta-item {{ margin: 5px 0; }}
            .meta-label {{ font-weight: bold; color: #667eea; }}
            .content {{ white-space: pre-wrap; font-family: 'Courier New', monospace; background: #fafafa; padding: 20px; border: 1px solid #e0e0e0; border-radius: 5px; }}
            .footer {{ margin-top: 40px; padding-top: 20px; border-top: 2px solid #e0e0e0; text-align: center; color: #999; font-size: 8pt; }}
            h1, h2, h3 {{ color: #667eea; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>{company_name}</h1>
            <p class="doc-type">{document.get('skill_display', 'Document')}</p>
        </div>
        <div class="meta">
            <div class="meta-item"><span class="meta-label">Customer:</span> {document['customer_name']}</div>
            {'<div class="meta-item"><span class="meta-label">Email:</span> ' + document['customer_email'] + '</div>' if document.get('customer_email') else ''}
            {'<div class="meta-item"><span class="meta-label">Phone:</span> ' + document['customer_phone'] + '</div>' if document.get('customer_phone') else ''}
            <div class="meta-item"><span class="meta-label">Generated:</span> {document['created_at']}</div>
            <div class="meta-item"><span class="meta-label">Document ID:</span> {document['id']}</div>
        </div>
        <div class="content">{document['content']}</div>
        <div class="footer"><p>Powered by ZettaBrain Skills</p></div>
    </body>
    </html>
    """

    pdf_bytes = BytesIO()
    HTML(string=pdf_html).write_pdf(pdf_bytes)
    pdf_bytes.seek(0)

    skill_name = document.get('skill_name', 'document').replace(' ', '-')
    return Response(
        content=pdf_bytes.read(),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=zettabrain-{skill_name}-{doc_id[:8]}.pdf"
        }
    )


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
    llm_status = provider.check_health()

    return {
        "status": "healthy" if llm_status else "degraded",
        "llm_provider": "running" if llm_status else "not running",
        "business_context_loaded": BUSINESS_CONTEXT is not None,
        "business_name": BUSINESS_INFO.company_name if BUSINESS_INFO else None,
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
