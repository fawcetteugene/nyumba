import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Any
from .crypto_utils import get_or_create_key, encrypt_text, decrypt_text

_DB_PATH = Path.home() / ".nyumba" / "nyumba.db"
_DB_PATH.parent.mkdir(exist_ok=True)

_fernet = None

def _get_fernet():
    global _fernet
    if _fernet is None:
        _fernet = get_or_create_key()
    return _fernet

def get_db():
    conn = sqlite3.connect(str(_DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS agreements (
                id TEXT PRIMARY KEY,
                encrypted_blob TEXT NOT NULL,
                location TEXT NOT NULL,
                participants TEXT NOT NULL,
                created_at REAL NOT NULL,
                verified INTEGER DEFAULT 0,
                synced INTEGER DEFAULT 0
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS witness_votes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agreement_id TEXT NOT NULL,
                vote INTEGER NOT NULL,
                note TEXT,
                witness_alias TEXT NOT NULL,
                created_at REAL NOT NULL,
                FOREIGN KEY(agreement_id) REFERENCES agreements(id)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS conflict_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agreement_id TEXT,
                risk_score REAL NOT NULL,
                topics TEXT NOT NULL,
                created_at REAL NOT NULL
            )
        """)
        conn.commit()

def save_agreement(id: str, encrypted_blob: str, location: str, participants: str, created_at: float, verified: int = 0, synced: int = 0):
    with get_db() as conn:
        conn.execute(
            "INSERT INTO agreements (id, encrypted_blob, location, participants, created_at, verified, synced) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (id, encrypted_blob, location, participants, created_at, verified, synced)
        )
        conn.commit()

def get_agreement(id: str) -> Dict[str, Any]:
    with get_db() as conn:
        row = conn.execute("SELECT * FROM agreements WHERE id = ?", (id,)).fetchone()
        if not row:
            return None
        return dict(row)

def save_witness_vote(agreement_id: str, vote: int, note: str, alias: str, created_at: float):
    with get_db() as conn:
        conn.execute(
            "INSERT INTO witness_votes (agreement_id, vote, note, witness_alias, created_at) VALUES (?, ?, ?, ?, ?)",
            (agreement_id, vote, note, alias, created_at)
        )
        conn.commit()

def count_yes_votes(agreement_id: str) -> int:
    with get_db() as conn:
        row = conn.execute("SELECT COUNT(*) as cnt FROM witness_votes WHERE agreement_id = ? AND vote = 1", (agreement_id,)).fetchone()
        return row["cnt"]

def mark_verified(agreement_id: str):
    with get_db() as conn:
        conn.execute("UPDATE agreements SET verified = 1 WHERE id = ?", (agreement_id,))
        conn.commit()

def get_all_agreements() -> List[Dict[str, Any]]:
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM agreements ORDER BY created_at DESC").fetchall()
        return [dict(row) for row in rows]

def save_conflict_report(agreement_id: str, risk_score: float, topics: str, created_at: float):
    with get_db() as conn:
        conn.execute(
            "INSERT INTO conflict_reports (agreement_id, risk_score, topics, created_at) VALUES (?, ?, ?, ?)",
            (agreement_id, risk_score, topics, created_at)
        )
        conn.commit()
