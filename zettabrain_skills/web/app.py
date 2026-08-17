"""
FastAPI web application for ZettaBrain Skills
Simple interface for Mike at 3RVA to generate quotes from customer requests
"""

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import os
from typing import Optional

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

# Store generated quotes in memory (for demo)
generated_quotes = []


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with quote generator form"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "3RVA Quote Generator"
    })


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
            return templates.TemplateResponse("error.html", {
                "request": request,
                "error": "Ollama is not running. Please start Ollama first.",
                "suggestion": "Run: ollama serve"
            })

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
            return templates.TemplateResponse("error.html", {
                "request": request,
                "error": f"Generation failed: {result.error}",
                "suggestion": "Please try again or check Ollama logs."
            })

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

        return templates.TemplateResponse("quote.html", {
            "request": request,
            "quote": quote_data
        })

    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": str(e),
            "suggestion": "Please check that Ollama is running and the skill file exists."
        })


@app.get("/quotes", response_class=HTMLResponse)
async def list_quotes(request: Request):
    """List all generated quotes"""
    return templates.TemplateResponse("quotes.html", {
        "request": request,
        "quotes": generated_quotes
    })


@app.get("/quote/{quote_id}", response_class=HTMLResponse)
async def view_quote(request: Request, quote_id: str):
    """View a specific quote"""
    quote = next((q for q in generated_quotes if q["id"] == quote_id), None)

    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")

    return templates.TemplateResponse("quote.html", {
        "request": request,
        "quote": quote
    })


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
