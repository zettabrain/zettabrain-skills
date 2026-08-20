"""
FastAPI web application for ZettaBrain Skills.
SPA architecture with JSON API + WebSocket streaming.
"""

import glob
import os
import time
import json
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, List, Optional

import markdown
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from weasyprint import HTML

from zettabrain_skills.core.engine import GenerationEngine
from zettabrain_skills.core.models import GenerationRequest
from zettabrain_skills.skills.parser import load_skill

app = FastAPI(
    title="ZettaBrain Skills",
    description="AI-powered document generation with skills",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

SKILLS_DIR = os.getenv("SKILLS_DIR", "examples")
CORPUS_PATH = os.getenv("CORPUS_PATH", ".corpus")

generated_documents: List[Dict[str, Any]] = []


def _load_skills() -> List[Dict[str, Any]]:
    skills = []
    for skill_file in sorted(glob.glob(f"{SKILLS_DIR}/*.md")):
        try:
            skill = load_skill(skill_file)
            skills.append({
                "file": skill_file,
                "name": skill.name,
                "display_name": skill.name.replace("-", " ").title(),
                "description": skill.description,
                "business_type": skill.business_type,
                "version": skill.version,
                "requires_corpus": skill.requires_corpus,
                "citation_required": skill.citation_required,
            })
        except Exception:
            continue
    return skills


def _get_engine() -> GenerationEngine:
    engine = GenerationEngine()
    corpus_path = Path(CORPUS_PATH)
    if corpus_path.exists():
        try:
            from zettabrain_skills.corpus.retrieval import CorpusRetriever
            engine.corpus_retriever = CorpusRetriever(corpus_path=str(corpus_path))
        except Exception:
            pass
    return engine


# ── Root: serve SPA ──────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def root():
    index = STATIC_DIR / "index.html"
    if index.exists():
        return HTMLResponse(index.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>ZettaBrain Skills</h1><p>Static files not found.</p>")


# ── API: Status ──────────────────────────────────────────

@app.get("/api/status")
async def api_status():
    from zettabrain_skills.llm.factory import create_llm_provider, get_provider_info

    provider = create_llm_provider()
    llm_healthy = provider.check_health()
    model_info = provider.get_model_info() if llm_healthy else {}
    provider_info = get_provider_info()

    corpus_chunks = 0
    corpus_docs = 0
    try:
        from zettabrain_skills.corpus.retrieval import CorpusRetriever
        corpus_path = Path(CORPUS_PATH)
        if corpus_path.exists() and (corpus_path / "manifest.json").exists():
            retriever = CorpusRetriever(corpus_path=str(corpus_path))
            corpus_chunks = retriever.chunk_count
            corpus_docs = retriever.document_count
    except Exception:
        pass

    return {
        "llm": {
            "healthy": llm_healthy,
            "provider": provider_info.get("provider", "unknown"),
            "model": model_info.get("model", "unknown"),
        },
        "skills": {
            "count": len(_load_skills()),
            "directory": SKILLS_DIR,
        },
        "corpus": {
            "chunks": corpus_chunks,
            "documents": corpus_docs,
            "path": CORPUS_PATH,
        },
        "documents_generated": len(generated_documents),
        "version": "1.0.0",
    }


# ── API: Skills ──────────────────────────────────────────

@app.get("/api/skills")
async def api_skills():
    return _load_skills()


# ── API: Generate ────────────────────────────────────────

class GenerateRequest(BaseModel):
    skill_file: str
    input_text: str
    customer_name: str = ""
    customer_email: str = ""
    customer_phone: str = ""


@app.post("/api/generate")
async def api_generate(req: GenerateRequest):
    skill_path = Path(req.skill_file)
    if not skill_path.exists():
        raise HTTPException(status_code=400, detail=f"Skill file not found: {req.skill_file}")

    skill = load_skill(str(skill_path))
    engine = _get_engine()

    if not engine.llm_provider.check_health():
        raise HTTPException(status_code=503, detail="LLM provider is not running")

    today = datetime.now()
    parts = [f"TODAY'S DATE: {today.strftime('%B %d, %Y')}\n\n"]
    if req.customer_name:
        parts.append(f"Customer/Client: {req.customer_name}\n")
    if req.customer_email:
        parts.append(f"Email: {req.customer_email}\n")
    if req.customer_phone:
        parts.append(f"Phone: {req.customer_phone}\n")
    if req.customer_name or req.customer_email or req.customer_phone:
        parts.append("\n")
    parts.append(req.input_text)

    gen_request = GenerationRequest(
        input="".join(parts),
        skill_name=skill.name,
        business_id="default",
    )

    result = engine.generate(skill, gen_request)

    if not result.success:
        raise HTTPException(status_code=500, detail=f"Generation failed: {result.error}")

    doc_data = {
        "id": result.id,
        "skill_name": skill.name,
        "skill_display": skill.name.replace("-", " ").title(),
        "customer_name": req.customer_name or "Customer",
        "customer_email": req.customer_email,
        "customer_phone": req.customer_phone,
        "request": req.input_text,
        "content": result.content,
        "citations": result.citations,
        "created_at": result.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "generation_time_ms": result.generation_time_ms,
    }
    generated_documents.insert(0, doc_data)
    if len(generated_documents) > 50:
        generated_documents.pop()

    return doc_data


# ── WebSocket: Streaming Generation ─────────────────────

@app.websocket("/ws/generate")
async def ws_generate(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()

            skill_file = data.get("skill_file")
            input_text = data.get("input_text", "")
            customer_name = data.get("customer_name", "")

            if not skill_file or not input_text:
                await websocket.send_json({"type": "error", "message": "skill_file and input_text required"})
                continue

            skill_path = Path(skill_file)
            if not skill_path.exists():
                await websocket.send_json({"type": "error", "message": f"Skill not found: {skill_file}"})
                continue

            try:
                skill = load_skill(str(skill_path))
                engine = _get_engine()

                if not engine.llm_provider.check_health():
                    await websocket.send_json({"type": "error", "message": "LLM provider is not running"})
                    continue

                await websocket.send_json({"type": "status", "message": "Generating..."})

                today = datetime.now()
                parts = [f"TODAY'S DATE: {today.strftime('%B %d, %Y')}\n\n"]
                if customer_name:
                    parts.append(f"Customer/Client: {customer_name}\n\n")
                parts.append(input_text)

                gen_request = GenerationRequest(
                    input="".join(parts),
                    skill_name=skill.name,
                    business_id="default",
                )

                # Stream tokens if provider supports it
                start_time = time.time()
                corpus_context = None
                citations = []

                if skill.requires_corpus and engine.corpus_retriever:
                    corpus_text, citation_objects = (
                        engine.corpus_retriever.get_context_for_generation(
                            query=input_text, n_results=5, min_relevance=0.3,
                        )
                    )
                    if corpus_text:
                        corpus_context = corpus_text
                        citations = [
                            f"{c.document_title}"
                            + (f" ({c.citation_ref})" if c.citation_ref else "")
                            for c in citation_objects
                        ]
                        await websocket.send_json({"type": "citations", "citations": citations})

                prompt = engine.build_prompt(skill, "".join(parts), gen_request.context, corpus_context)

                temperature = skill.temperature
                max_tokens = skill.max_tokens

                try:
                    for token in engine.llm_provider.stream(
                        prompt=prompt, temperature=temperature, max_tokens=max_tokens
                    ):
                        await websocket.send_json({"type": "token", "token": token})
                except NotImplementedError:
                    content = engine.llm_provider.generate(
                        prompt=prompt, temperature=temperature, max_tokens=max_tokens
                    )
                    await websocket.send_json({"type": "token", "token": content})

                generation_time_ms = int((time.time() - start_time) * 1000)

                await websocket.send_json({
                    "type": "done",
                    "skill": skill.name,
                    "generation_time_ms": generation_time_ms,
                    "model": getattr(engine.llm_provider, "model", "unknown"),
                    "citations": citations,
                })

            except Exception as e:
                await websocket.send_json({"type": "error", "message": str(e)})

    except WebSocketDisconnect:
        pass


# ── API: Documents ───────────────────────────────────────

@app.get("/api/documents")
async def api_documents():
    return generated_documents


@app.get("/api/documents/{doc_id}")
async def api_document(doc_id: str):
    doc = next((d for d in generated_documents if d["id"] == doc_id), None)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


@app.get("/api/documents/{doc_id}/pdf")
async def api_document_pdf(doc_id: str):
    doc = next((d for d in generated_documents if d["id"] == doc_id), None)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    pdf_html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
@page {{ size: letter; margin: 0.75in; }}
body {{ font-family: Arial, sans-serif; font-size: 11pt; line-height: 1.6; color: #333; }}
.header {{ text-align: center; margin-bottom: 30px; border-bottom: 3px solid #6366f1; padding-bottom: 20px; }}
.header h1 {{ color: #6366f1; font-size: 22pt; margin: 0 0 8px 0; }}
.header .doc-type {{ color: #888; font-size: 11pt; font-style: italic; }}
.meta {{ background: #f8f9ff; padding: 15px; margin-bottom: 25px; border-left: 4px solid #6366f1; }}
.meta-item {{ margin: 4px 0; }}
.meta-label {{ font-weight: bold; color: #6366f1; }}
.content {{ white-space: pre-wrap; }}
.footer {{ margin-top: 40px; border-top: 1px solid #ddd; padding-top: 12px; text-align: center; color: #999; font-size: 8pt; }}
</style></head><body>
<div class="header">
  <h1>ZettaBrain Skills</h1>
  <p class="doc-type">{doc.get('skill_display', 'Document')}</p>
</div>
<div class="meta">
  <div class="meta-item"><span class="meta-label">Customer:</span> {doc['customer_name']}</div>
  <div class="meta-item"><span class="meta-label">Generated:</span> {doc['created_at']}</div>
  <div class="meta-item"><span class="meta-label">ID:</span> {doc['id']}</div>
</div>
<div class="content">{doc['content']}</div>
<div class="footer">Powered by ZettaBrain Skills</div>
</body></html>"""

    pdf_bytes = BytesIO()
    HTML(string=pdf_html).write_pdf(pdf_bytes)
    pdf_bytes.seek(0)

    skill_name = doc.get("skill_name", "document").replace(" ", "-")
    return Response(
        content=pdf_bytes.read(),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=zettabrain-{skill_name}-{doc_id[:8]}.pdf"},
    )


# ── API: Corpus ──────────────────────────────────────────

@app.get("/api/corpus/status")
async def api_corpus_status():
    try:
        from zettabrain_skills.corpus.retrieval import CorpusRetriever
        corpus_path = Path(CORPUS_PATH)
        if not corpus_path.exists() or not (corpus_path / "manifest.json").exists():
            return {"configured": False, "chunks": 0, "documents": 0}

        retriever = CorpusRetriever(corpus_path=str(corpus_path))
        manifest = retriever.ingestor.get_manifest()

        docs = [
            {"title": d.title, "type": d.file_type, "chunks": d.chunk_count, "status": d.status.value}
            for d in manifest.documents
        ]
        return {
            "configured": True,
            "chunks": retriever.chunk_count,
            "documents": retriever.document_count,
            "document_list": docs,
        }
    except Exception as e:
        return {"configured": False, "error": str(e)}


class CorpusSearchRequest(BaseModel):
    query: str
    n_results: int = 5


@app.post("/api/corpus/search")
async def api_corpus_search(req: CorpusSearchRequest):
    from zettabrain_skills.corpus.retrieval import CorpusRetriever

    corpus_path = Path(CORPUS_PATH)
    if not corpus_path.exists():
        raise HTTPException(status_code=400, detail="No corpus configured")

    retriever = CorpusRetriever(corpus_path=str(corpus_path))
    results = retriever.search(req.query, n_results=req.n_results)

    return [
        {
            "title": r.citation.document_title,
            "excerpt": r.chunk.content[:300],
            "score": round(r.score, 3),
            "citation_ref": r.citation.citation_ref,
            "issuing_body": r.citation.issuing_body,
        }
        for r in results
    ]


# ── API: Corpus Upload ──────────────────────────────────

CORPUS_SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt", ".md"}


@app.post("/api/corpus/upload")
async def api_corpus_upload(files: List[UploadFile] = File(...)):
    """Upload and ingest documents into the corpus."""
    from zettabrain_skills.corpus.retrieval import CorpusRetriever

    corpus_path = Path(CORPUS_PATH)
    upload_dir = corpus_path / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)

    saved_files = []
    skipped_files = []

    for file in files:
        ext = Path(file.filename).suffix.lower()
        if ext not in CORPUS_SUPPORTED_EXTENSIONS:
            skipped_files.append({"name": file.filename, "reason": f"Unsupported format: {ext}"})
            continue

        dest = upload_dir / file.filename
        content = await file.read()
        dest.write_bytes(content)
        saved_files.append(str(dest))

    if not saved_files:
        return {
            "ingested": 0,
            "skipped": skipped_files,
            "error": "No supported files to ingest",
        }

    retriever = CorpusRetriever(corpus_path=str(corpus_path))
    ingested_count = 0

    for file_path in saved_files:
        count = retriever.ingest(Path(file_path))
        ingested_count += count

    return {
        "ingested": ingested_count,
        "total_documents": retriever.document_count,
        "total_chunks": retriever.chunk_count,
        "skipped": skipped_files,
    }


# ── API: Skills Upload ──────────────────────────────────

@app.post("/api/skills/upload")
async def api_skills_upload(file: UploadFile = File(...)):
    """Upload a new skill file (.md with YAML frontmatter)."""
    if not file.filename.endswith(".md"):
        raise HTTPException(status_code=400, detail="Skill files must be .md format")

    content = await file.read()
    text = content.decode("utf-8")

    if not text.startswith("---"):
        raise HTTPException(
            status_code=400,
            detail="Invalid skill file: must start with YAML frontmatter (---)",
        )

    skills_dir = Path(SKILLS_DIR)
    skills_dir.mkdir(parents=True, exist_ok=True)

    dest = skills_dir / file.filename
    dest.write_text(text, encoding="utf-8")

    try:
        skill = load_skill(str(dest))
        return {
            "success": True,
            "file": str(dest),
            "name": skill.name,
            "display_name": skill.name.replace("-", " ").title(),
            "description": skill.description,
            "version": skill.version,
            "requires_corpus": skill.requires_corpus,
        }
    except Exception as e:
        dest.unlink(missing_ok=True)
        raise HTTPException(status_code=400, detail=f"Invalid skill file: {e}")


@app.delete("/api/skills/{skill_name}")
async def api_delete_skill(skill_name: str):
    """Delete a skill file by name."""
    skills_dir = Path(SKILLS_DIR)
    for skill_file in skills_dir.glob("*.md"):
        try:
            skill = load_skill(str(skill_file))
            if skill.name == skill_name:
                skill_file.unlink()
                return {"deleted": True, "name": skill_name}
        except Exception:
            continue
    raise HTTPException(status_code=404, detail=f"Skill not found: {skill_name}")


# ── Health ───────────────────────────────────────────────

@app.get("/health")
async def health_check():
    from zettabrain_skills.llm.factory import create_llm_provider
    provider = create_llm_provider()
    healthy = provider.check_health()
    return {"status": "healthy" if healthy else "degraded", "version": "1.0.0"}
