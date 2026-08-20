"""Corpus retrieval - semantic search with citation generation."""

import json
import os
from pathlib import Path
from typing import List, Optional

from zettabrain_skills.corpus.ingest import DocumentIngestor
from zettabrain_skills.corpus.models import (
    Citation,
    CorpusDocument,
    DocumentChunk,
    SearchResult,
)
from zettabrain_skills.corpus.store import VectorStore


class CorpusRetriever:
    """High-level interface for corpus search and citation generation."""

    def __init__(
        self,
        corpus_path: Optional[str] = None,
        store_path: Optional[str] = None,
        collection_name: str = "corpus",
        embedding_model: str = "nomic-embed-text",
        ollama_url: Optional[str] = None,
    ):
        self.corpus_path = Path(
            corpus_path or os.getenv("CORPUS_PATH", ".corpus")
        )
        self.store_path = store_path or os.getenv(
            "CORPUS_STORE_PATH", str(self.corpus_path / "vectorstore")
        )

        self.store = VectorStore(
            persist_path=self.store_path,
            collection_name=collection_name,
            embedding_model=embedding_model,
            ollama_url=ollama_url,
        )

        self.ingestor = DocumentIngestor(corpus_path=self.corpus_path)

    @property
    def document_count(self) -> int:
        return self.ingestor.get_manifest().document_count

    @property
    def chunk_count(self) -> int:
        return self.store.count

    def ingest(self, path: Path) -> int:
        """Ingest a file or directory into the corpus and vector store.

        Returns number of new documents ingested.
        """
        path = Path(path)

        if path.is_file():
            result = self.ingestor.ingest_file(path)
            if result:
                _, chunks = result
                self.store.add_chunks(chunks)
                return 1
            return 0

        results = self.ingestor.ingest_directory(path)
        for _, chunks in results:
            self.store.add_chunks(chunks)
        return len(results)

    def search(
        self,
        query: str,
        n_results: int = 5,
        min_relevance: float = 0.0,
    ) -> List[SearchResult]:
        """Search the corpus and return results with citations."""
        raw_results = self.store.search(query, n_results=n_results)

        search_results = []
        for hit in raw_results:
            score = 1.0 - hit["distance"]
            if score < min_relevance:
                continue

            metadata = hit["metadata"]
            document_id = metadata.get("document_id", "")

            doc = self.ingestor.get_manifest().get_document(document_id)

            chunk = DocumentChunk(
                id=hit["id"],
                document_id=document_id,
                content=hit["document"],
                chunk_index=int(metadata.get("chunk_index", 0)),
                start_char=int(metadata.get("start_char", 0)),
                end_char=int(metadata.get("end_char", 0)),
                metadata=metadata,
            )

            citation = Citation(
                document_id=document_id,
                document_title=metadata.get("document_title", "Unknown"),
                chunk_id=hit["id"],
                chunk_index=chunk.chunk_index,
                relevance_score=score,
                excerpt=hit["document"][:200],
                source_path=metadata.get("source_path", ""),
                issuing_body=doc.issuing_body if doc else None,
                citation_ref=doc.citation_ref if doc else None,
                effective_date=doc.effective_date if doc else None,
            )

            search_results.append(SearchResult(
                chunk=chunk,
                score=score,
                citation=citation,
            ))

        return search_results

    def get_context_for_generation(
        self,
        query: str,
        n_results: int = 5,
        min_relevance: float = 0.3,
    ) -> tuple[str, List[Citation]]:
        """Retrieve corpus context formatted for prompt injection.

        Returns (context_text, citations).
        """
        results = self.search(query, n_results=n_results, min_relevance=min_relevance)

        if not results:
            return "", []

        context_parts = ["# CORPUS CONTEXT", ""]
        context_parts.append(
            "The following excerpts are from verified source documents. "
            "Use ONLY this information to inform your response. "
            "If the answer is not covered below, state that explicitly."
        )
        context_parts.append("")

        citations = []
        for i, result in enumerate(results, 1):
            c = result.citation
            context_parts.append(f"## Source {i}: {c.document_title}")
            if c.citation_ref:
                context_parts.append(f"Reference: {c.citation_ref}")
            if c.issuing_body:
                context_parts.append(f"Issued by: {c.issuing_body}")
            if c.effective_date:
                context_parts.append(f"Effective: {c.effective_date}")
            context_parts.append("")
            context_parts.append(result.chunk.content)
            context_parts.append("")
            citations.append(c)

        context_parts.append("---")
        context_parts.append(
            "When referencing the above, cite the source by title and reference number."
        )

        return "\n".join(context_parts), citations

    def reset(self) -> None:
        """Clear the vector store. Does not delete the manifest."""
        self.store.reset()
