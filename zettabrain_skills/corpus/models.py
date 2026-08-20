"""Data models for corpus management."""

import hashlib
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class DocumentStatus(str, Enum):
    CURRENT = "current"
    SUPERSEDED = "superseded"
    PENDING = "pending"


class CorpusDocument(BaseModel):
    """A source document ingested into the corpus."""

    id: str
    title: str
    source_path: str
    content_hash: str
    issuing_body: Optional[str] = None
    citation_ref: Optional[str] = None
    source_url: Optional[str] = None
    retrieved_at: Optional[datetime] = None
    effective_date: Optional[str] = None
    status: DocumentStatus = DocumentStatus.CURRENT
    review_by: Optional[str] = None
    corpus_version: str = "1"
    file_type: str = "unknown"
    chunk_count: int = 0
    ingested_at: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, str] = Field(default_factory=dict)

    @staticmethod
    def compute_hash(content: str) -> str:
        return hashlib.sha256(content.encode()).hexdigest()


class DocumentChunk(BaseModel):
    """A chunk of a document stored in the vector database."""

    id: str
    document_id: str
    content: str
    chunk_index: int
    start_char: int
    end_char: int
    metadata: Dict[str, str] = Field(default_factory=dict)


class Citation(BaseModel):
    """A citation linking generated content back to a source chunk."""

    document_id: str
    document_title: str
    chunk_id: str
    chunk_index: int
    relevance_score: float
    excerpt: str
    source_path: str
    issuing_body: Optional[str] = None
    citation_ref: Optional[str] = None
    effective_date: Optional[str] = None


class SearchResult(BaseModel):
    """A single search result from corpus retrieval."""

    chunk: DocumentChunk
    score: float
    citation: Citation


class CorpusManifest(BaseModel):
    """Tracks all documents in a corpus for auditability."""

    corpus_id: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    documents: List[CorpusDocument] = Field(default_factory=list)

    @property
    def document_count(self) -> int:
        return len(self.documents)

    @property
    def current_documents(self) -> List[CorpusDocument]:
        return [d for d in self.documents if d.status == DocumentStatus.CURRENT]

    def get_document(self, document_id: str) -> Optional[CorpusDocument]:
        return next((d for d in self.documents if d.id == document_id), None)

    def has_document(self, content_hash: str) -> bool:
        return any(d.content_hash == content_hash for d in self.documents)
