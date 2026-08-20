"""Persistent document storage using SQLite."""

import json
import os
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional


DEFAULT_DB_PATH = ".data/documents.db"


class DocumentStore:
    """SQLite-backed store for generated documents."""

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or os.getenv("DOCUMENTS_DB_PATH", DEFAULT_DB_PATH)
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self):
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id TEXT PRIMARY KEY,
                skill_name TEXT NOT NULL,
                skill_display TEXT NOT NULL,
                customer_name TEXT DEFAULT '',
                customer_email TEXT DEFAULT '',
                customer_phone TEXT DEFAULT '',
                request TEXT NOT NULL,
                content TEXT NOT NULL,
                citations TEXT DEFAULT '[]',
                created_at TEXT NOT NULL,
                generation_time_ms INTEGER DEFAULT 0
            )
        """)
        self._conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_documents_created_at
            ON documents(created_at DESC)
        """)
        self._conn.commit()

    def insert(self, doc: Dict[str, Any]) -> None:
        self._conn.execute("""
            INSERT OR REPLACE INTO documents
            (id, skill_name, skill_display, customer_name, customer_email,
             customer_phone, request, content, citations, created_at, generation_time_ms)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            doc["id"],
            doc["skill_name"],
            doc["skill_display"],
            doc.get("customer_name", ""),
            doc.get("customer_email", ""),
            doc.get("customer_phone", ""),
            doc.get("request", ""),
            doc["content"],
            json.dumps(doc.get("citations", [])),
            doc["created_at"],
            doc.get("generation_time_ms", 0),
        ))
        self._conn.commit()

    def get_all(self, limit: int = 50) -> List[Dict[str, Any]]:
        cursor = self._conn.execute(
            "SELECT * FROM documents ORDER BY created_at DESC LIMIT ?", (limit,)
        )
        return [self._row_to_dict(row) for row in cursor.fetchall()]

    def get_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        cursor = self._conn.execute(
            "SELECT * FROM documents WHERE id = ?", (doc_id,)
        )
        row = cursor.fetchone()
        return self._row_to_dict(row) if row else None

    def delete(self, doc_id: str) -> None:
        self._conn.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
        self._conn.commit()

    def count(self) -> int:
        cursor = self._conn.execute("SELECT COUNT(*) FROM documents")
        return cursor.fetchone()[0]

    def _row_to_dict(self, row: sqlite3.Row) -> Dict[str, Any]:
        d = dict(row)
        d["citations"] = json.loads(d["citations"])
        return d
