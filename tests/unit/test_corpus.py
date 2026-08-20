"""Tests for the corpus module - ingestion, chunking, and metadata parsing."""

import json
import pytest
from pathlib import Path

from zettabrain_skills.corpus.models import (
    CorpusDocument,
    CorpusManifest,
    DocumentChunk,
    DocumentStatus,
    Citation,
    SearchResult,
)
from zettabrain_skills.corpus.ingest import (
    chunk_text,
    parse_metadata_header,
    DocumentIngestor,
)


class TestModels:
    def test_corpus_document_hash(self):
        hash1 = CorpusDocument.compute_hash("hello world")
        hash2 = CorpusDocument.compute_hash("hello world")
        hash3 = CorpusDocument.compute_hash("different content")

        assert hash1 == hash2
        assert hash1 != hash3

    def test_corpus_manifest_operations(self):
        manifest = CorpusManifest(corpus_id="test-corpus")

        assert manifest.document_count == 0
        assert manifest.current_documents == []
        assert manifest.get_document("nonexistent") is None

        doc = CorpusDocument(
            id="doc-1",
            title="Test Doc",
            source_path="/tmp/test.pdf",
            content_hash="abc123",
            status=DocumentStatus.CURRENT,
        )
        manifest.documents.append(doc)

        assert manifest.document_count == 1
        assert len(manifest.current_documents) == 1
        assert manifest.get_document("doc-1") == doc
        assert manifest.has_document("abc123") is True
        assert manifest.has_document("xyz789") is False

    def test_manifest_filters_superseded(self):
        manifest = CorpusManifest(corpus_id="test")

        manifest.documents.append(CorpusDocument(
            id="1", title="Current", source_path="/a", content_hash="h1",
            status=DocumentStatus.CURRENT,
        ))
        manifest.documents.append(CorpusDocument(
            id="2", title="Old", source_path="/b", content_hash="h2",
            status=DocumentStatus.SUPERSEDED,
        ))

        assert manifest.document_count == 2
        assert len(manifest.current_documents) == 1
        assert manifest.current_documents[0].title == "Current"


class TestChunking:
    def test_empty_text(self):
        assert chunk_text("") == []

    def test_short_text_single_chunk(self):
        text = "Short text that fits in one chunk."
        chunks = chunk_text(text, chunk_size=1000, chunk_overlap=200)
        assert len(chunks) == 1
        assert chunks[0][0] == text
        assert chunks[0][1] == 0

    def test_long_text_multiple_chunks(self):
        text = "word " * 500
        chunks = chunk_text(text, chunk_size=100, chunk_overlap=20)
        assert len(chunks) > 1

        for chunk_text_content, start, end in chunks:
            assert len(chunk_text_content) > 0
            assert start >= 0
            assert end > start

    def test_chunks_have_overlap(self):
        paragraphs = ["Paragraph one content here. " * 10]
        paragraphs.append("\n\n")
        paragraphs.append("Paragraph two content here. " * 10)
        text = "".join(paragraphs)

        chunks = chunk_text(text, chunk_size=100, chunk_overlap=30)
        assert len(chunks) >= 2

    def test_respects_paragraph_boundaries(self):
        text = "First paragraph content.\n\nSecond paragraph content."
        chunks = chunk_text(text, chunk_size=30, chunk_overlap=5)
        assert len(chunks) >= 2


class TestMetadataHeader:
    def test_no_header(self):
        content = "Just plain text without any header."
        metadata, body = parse_metadata_header(content)
        assert metadata == {}
        assert body == content

    def test_valid_header(self):
        content = """=== CORPUS DOCUMENT ===
Title:            EPA Section 608 Regulations
Issuing body:     EPA
Citation:         40 CFR Part 82
Source URL:       https://example.com/doc.pdf
Retrieved:        2024-01-15
Effective date:   2024-01-01
Status:           current
Corpus version:   v2
Review by:        2024-07-15
=======================

This is the body content of the document.
It has multiple lines."""

        metadata, body = parse_metadata_header(content)

        assert metadata["title"] == "EPA Section 608 Regulations"
        assert metadata["issuing_body"] == "EPA"
        assert metadata["citation"] == "40 CFR Part 82"
        assert metadata["source_url"] == "https://example.com/doc.pdf"
        assert metadata["status"] == "current"
        assert metadata["corpus_version"] == "v2"
        assert "body content" in body

    def test_partial_header(self):
        content = """=== CORPUS DOCUMENT ===
Title: Quick Reference
Status: current
=======================

Body text here."""

        metadata, body = parse_metadata_header(content)
        assert metadata["title"] == "Quick Reference"
        assert metadata["status"] == "current"
        assert "Body text here." in body


class TestDocumentIngestor:
    def test_ingest_txt_file(self, tmp_path):
        corpus_dir = tmp_path / "corpus"
        corpus_dir.mkdir()

        doc_file = tmp_path / "test.txt"
        doc_file.write_text("This is test content for ingestion testing purposes. " * 5)

        ingestor = DocumentIngestor(corpus_path=corpus_dir)
        result = ingestor.ingest_file(doc_file)

        assert result is not None
        doc, chunks = result
        assert doc.title == "test"
        assert doc.file_type == "txt"
        assert doc.chunk_count > 0
        assert len(chunks) > 0

    def test_ingest_markdown_with_header(self, tmp_path):
        corpus_dir = tmp_path / "corpus"
        corpus_dir.mkdir()

        doc_file = tmp_path / "regulations.md"
        doc_file.write_text("""=== CORPUS DOCUMENT ===
Title:            Test Regulation
Issuing body:     Test Agency
Status:           current
=======================

# Section 1

This is the regulation body content that is long enough to be meaningful.
It contains multiple paragraphs and sections for proper chunking.

# Section 2

More content here to ensure we get multiple chunks from this document.
""")

        ingestor = DocumentIngestor(corpus_path=corpus_dir)
        result = ingestor.ingest_file(doc_file)

        assert result is not None
        doc, chunks = result
        assert doc.title == "Test Regulation"
        assert doc.issuing_body == "Test Agency"
        assert doc.status == DocumentStatus.CURRENT

    def test_incremental_ingestion_skips_unchanged(self, tmp_path):
        corpus_dir = tmp_path / "corpus"
        corpus_dir.mkdir()

        doc_file = tmp_path / "test.txt"
        doc_file.write_text("Same content for the incremental ingestion test. " * 10)

        ingestor = DocumentIngestor(corpus_path=corpus_dir)

        result1 = ingestor.ingest_file(doc_file)
        assert result1 is not None

        result2 = ingestor.ingest_file(doc_file)
        assert result2 is None

    def test_ingest_directory(self, tmp_path):
        corpus_dir = tmp_path / "corpus"
        corpus_dir.mkdir()

        docs_dir = tmp_path / "documents"
        docs_dir.mkdir()

        (docs_dir / "doc1.txt").write_text("First document with enough content. " * 5)
        (docs_dir / "doc2.md").write_text("Second document with markdown content. " * 5)
        (docs_dir / "ignored.json").write_text('{"not": "supported"}')

        ingestor = DocumentIngestor(corpus_path=corpus_dir)
        results = ingestor.ingest_directory(docs_dir)

        assert len(results) == 2

    def test_unsupported_file_skipped(self, tmp_path):
        corpus_dir = tmp_path / "corpus"
        corpus_dir.mkdir()

        doc_file = tmp_path / "data.csv"
        doc_file.write_text("col1,col2\nval1,val2")

        ingestor = DocumentIngestor(corpus_path=corpus_dir)
        result = ingestor.ingest_file(doc_file)
        assert result is None

    def test_manifest_persisted(self, tmp_path):
        corpus_dir = tmp_path / "corpus"
        corpus_dir.mkdir()

        doc_file = tmp_path / "test.txt"
        doc_file.write_text("Persistent manifest test content. " * 10)

        ingestor = DocumentIngestor(corpus_path=corpus_dir)
        ingestor.ingest_file(doc_file)

        manifest_path = corpus_dir / "manifest.json"
        assert manifest_path.exists()

        data = json.loads(manifest_path.read_text())
        assert len(data["documents"]) == 1
