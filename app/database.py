import sqlite3
from contextlib import contextmanager
from pathlib import Path

from app.config import settings


def get_db_path() -> str:
    """Extract file path from sqlite URL."""
    url = settings.database_url
    if url.startswith("sqlite:///"):
        return url.replace("sqlite:///", "")
    return "deepfakeguard.db"


def init_db():
    """Create tables if they don't exist."""
    db_path = get_db_path()
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS scans (
                id TEXT PRIMARY KEY,
                media_type TEXT NOT NULL,
                verdict TEXT NOT NULL,
                confidence REAL NOT NULL,
                severity TEXT NOT NULL,
                filename TEXT,
                ai_explanation TEXT,
                mitre_atlas TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


@contextmanager
def get_connection():
    """Context manager for SQLite connections."""
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def insert_scan(scan: dict):
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO scans (id, media_type, verdict, confidence, severity, filename, ai_explanation, mitre_atlas)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                scan["id"],
                scan["media_type"],
                scan["verdict"],
                scan["confidence"],
                scan["severity"],
                scan.get("filename"),
                scan.get("ai_explanation"),
                scan.get("mitre_atlas"),
            ),
        )
        conn.commit()


def get_scans(
    media_type: str | None = None,
    verdict: str | None = None,
    severity: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> tuple[list[dict], int]:
    with get_connection() as conn:
        query = "SELECT * FROM scans WHERE 1=1"
        params: list = []

        if media_type:
            query += " AND media_type = ?"
            params.append(media_type)
        if verdict:
            query += " AND verdict = ?"
            params.append(verdict)
        if severity:
            query += " AND severity = ?"
            params.append(severity)

        # Count
        count_row = conn.execute(query.replace("SELECT *", "SELECT COUNT(*)"), params).fetchone()
        total = count_row[0] if count_row else 0

        # Fetch
        query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        rows = conn.execute(query, params).fetchall()

        scans = [
            {
                "id": row["id"],
                "media_type": row["media_type"],
                "verdict": row["verdict"],
                "confidence": row["confidence"],
                "severity": row["severity"],
                "filename": row["filename"],
                "timestamp": row["created_at"],
            }
            for row in rows
        ]
        return scans, total


def get_scan_by_id(scan_id: str) -> dict | None:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM scans WHERE id = ?", (scan_id,)).fetchone()
        if not row:
            return None
        return dict(row)
