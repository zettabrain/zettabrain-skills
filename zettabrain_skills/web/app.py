"""
FastAPI web application for ZettaBrain Skills
Simple interface for Mike at 3RVA to generate quotes from customer requests
"""

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import os
import markdown
from typing import Optional
from weasyprint import HTML, CSS
from io import BytesIO

from zettabrain_skills.skills.parser import load_skill
from zettabrain_skills.core.engine import GenerationEngine
from zettabrain_skills.core.models import GenerationRequest

# Initialize FastAPI app
app = FastAPI(
    title="ZettaBrain Skills - Quote Generator",
    description="Generate professional quotes from customer requests",
    version="0.4.0"
)

# Setup templates directory
BASE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Mount static files
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Store generated quotes in memory (for demo)
generated_quotes = []


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with quote generator form"""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"title": "3RVA Quote Generator"}
    )


@app.post("/generate", response_class=HTMLResponse)
async def generate_quote(
    request: Request,
    customer_request: str = Form(...),
    customer_name: str = Form(""),
    customer_email: str = Form(""),
    customer_phone: str = Form("")
):
    """Generate a quote from customer request"""

    try:
        # Find the skill file
        skill_path = Path("examples/3rva-quote-full.md")
        if not skill_path.exists():
            # Try relative to current working directory
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

        # Build enhanced request with customer details
        enhanced_request = customer_request
        if customer_name:
            enhanced_request = f"Customer: {customer_name}\n{enhanced_request}"
        if customer_email:
            enhanced_request = f"{enhanced_request}\nEmail: {customer_email}"
        if customer_phone:
            enhanced_request = f"{enhanced_request}\nPhone: {customer_phone}"

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
            "customer_name": customer_name or "Customer",
            "customer_email": customer_email,
            "customer_phone": customer_phone,
            "request": customer_request,
            "quote": result.content,
            "created_at": result.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "generation_time": f"{result.generation_time_ms / 1000:.1f}s"
        }
        generated_quotes.insert(0, quote_data)  # Add to front

        # Keep only last 50 quotes
        if len(generated_quotes) > 50:
            generated_quotes.pop()

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


@app.get("/quotes", response_class=HTMLResponse)
async def list_quotes(request: Request):
    """List all generated quotes"""
    return templates.TemplateResponse(
        request=request,
        name="quotes.html",
        context={"quotes": generated_quotes}
    )


@app.get("/quote/{quote_id}", response_class=HTMLResponse)
async def view_quote(request: Request, quote_id: str):
    """View a specific quote"""
    quote = next((q for q in generated_quotes if q["id"] == quote_id), None)

    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")

    return templates.TemplateResponse(
        request=request,
        name="quote.html",
        context={"quote": quote}
    )


@app.get("/quote/{quote_id}/pdf")
async def download_pdf(quote_id: str):
    """Download quote as PDF"""
    quote = next((q for q in generated_quotes if q["id"] == quote_id), None)

    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")

    # Convert markdown to HTML
    md = markdown.Markdown(extensions=['extra', 'nl2br'])
    quote_html = md.convert(quote['quote'])

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
                border-bottom: 3px solid #667eea;
                padding-bottom: 20px;
            }}
            .header h1 {{
                color: #667eea;
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
                border-left: 4px solid #667eea;
            }}
            .meta-item {{
                margin: 5px 0;
            }}
            .meta-label {{
                font-weight: bold;
                color: #667eea;
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
                color: #667eea;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🧊 3RVA REFRIGERANT SUPPLY</h1>
            <p>Professional HVAC Refrigerant Solutions</p>
            <p>Richmond Metro Area | (804) 555-3RVA</p>
        </div>

        <div class="meta">
            <div class="meta-item">
                <span class="meta-label">Customer:</span> {quote['customer_name']}
            </div>
            {'<div class="meta-item"><span class="meta-label">Email:</span> ' + quote['customer_email'] + '</div>' if quote.get('customer_email') else ''}
            {'<div class="meta-item"><span class="meta-label">Phone:</span> ' + quote['customer_phone'] + '</div>' if quote.get('customer_phone') else ''}
            <div class="meta-item">
                <span class="meta-label">Generated:</span> {quote['created_at']}
            </div>
            <div class="meta-item">
                <span class="meta-label">Quote ID:</span> {quote['id']}
            </div>
        </div>

        <div class="content">
{quote['quote']}
        </div>

        <div class="footer">
            <p>Generated by ZettaBrain Skills | This quote is valid for 7 days</p>
            <p>3RVA Refrigerant Supply | Richmond, VA | www.3rva.com</p>
        </div>
    </body>
    </html>
    """

    # Generate PDF
    pdf_bytes = BytesIO()
    HTML(string=pdf_html).write_pdf(pdf_bytes)
    pdf_bytes.seek(0)

    # Return PDF
    return Response(
        content=pdf_bytes.read(),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=3rva-quote-{quote_id[:8]}.pdf"
        }
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
        "version": "0.4.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
