"""Vector store - ChromaDB wrapper for document chunk storage and retrieval."""

import os
from pathlib import Path
from typing import List, Optional

import chromadb
import httpx

from zettabrain_skills.corpus.models import DocumentChunk


class OllamaEmbeddingFunction:
    """Embedding function using Ollama's API."""

    def __init__(
        self,
        model: str = "nomic-embed-text",
        base_url: str = "http://localhost:11434",
    ):
        self.model = model
        self.base_url = base_url

    def __call__(self, input: List[str]) -> List[List[float]]:
        embeddings = []
        for text in input:
            try:
                response = httpx.post(
                    f"{self.base_url}/api/embed",
                    json={"model": self.model, "input": text},
                    timeout=60.0,
                )
                response.raise_for_status()
                data = response.json()
                embeddings.append(data["embeddings"][0])
            except httpx.HTTPStatusError:
                response = httpx.post(
                    f"{self.base_url}/api/embeddings",
                    json={"model": self.model, "prompt": text},
                    timeout=60.0,
                )
                response.raise_for_status()
                data = response.json()
                embeddings.append(data["embedding"])
        return embeddings


class VectorStore:
    """ChromaDB-based vector store for corpus document chunks."""

    def __init__(
        self,
        persist_path: Optional[str] = None,
        collection_name: str = "corpus",
        embedding_model: str = "nomic-embed-text",
        ollama_url: Optional[str] = None,
    ):
        self.persist_path = persist_path or os.getenv(
            "CORPUS_STORE_PATH", ".corpus_store"
        )
        self.collection_name = collection_name
        self.ollama_url = ollama_url or os.getenv(
            "OLLAMA_HOST", "http://localhost:11434"
        )

        Path(self.persist_path).mkdir(parents=True, exist_ok=True)

        self._embedding_fn = OllamaEmbeddingFunction(
            model=embedding_model,
            base_url=self.ollama_url,
        )

        self._client = chromadb.PersistentClient(path=self.persist_path)
        self._collection = self._client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self._embedding_fn,
            metadata={"hnsw:space": "cosine"},
        )

    @property
    def count(self) -> int:
        return self._collection.count()

    def add_chunks(self, chunks: List[DocumentChunk]) -> None:
        """Add document chunks to the vector store."""
        if not chunks:
            return

        self._collection.add(
            ids=[c.id for c in chunks],
            documents=[c.content for c in chunks],
            metadatas=[
                {
                    "document_id": c.document_id,
                    "chunk_index": c.chunk_index,
                    "start_char": c.start_char,
                    "end_char": c.end_char,
                    **c.metadata,
                }
                for c in chunks
            ],
        )

    def search(
        self,
        query: str,
        n_results: int = 5,
        where: Optional[dict] = None,
    ) -> List[dict]:
        """Search for relevant chunks.

        Returns list of dicts with keys: id, document, metadata, distance.
        """
        kwargs = {
            "query_texts": [query],
            "n_results": min(n_results, self.count) if self.count > 0 else 1,
        }
        if where:
            kwargs["where"] = where

        if self.count == 0:
            return []

        results = self._collection.query(**kwargs)

        hits = []
        for i in range(len(results["ids"][0])):
            hits.append({
                "id": results["ids"][0][i],
                "document": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i],
            })

        return hits

    def delete_by_document(self, document_id: str) -> None:
        """Remove all chunks for a given document."""
        self._collection.delete(where={"document_id": document_id})

    def reset(self) -> None:
        """Delete all data from the collection."""
        self._client.delete_collection(self.collection_name)
        self._collection = self._client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self._embedding_fn,
            metadata={"hnsw:space": "cosine"},
        )
