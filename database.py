#!/usr/bin/env python3
"""
AI-EDU-CZ — SQLite databáze
Tabulky: items, generated, published
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent / "data" / "aieducz.db"


def get_db() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    with get_db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS items (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                url         TEXT    UNIQUE NOT NULL,
                url_hash    TEXT    UNIQUE NOT NULL,
                title       TEXT    NOT NULL,
                source      TEXT    NOT NULL,
                published_at TEXT,
                fetched_at  TEXT    NOT NULL,
                content     TEXT,
                summary     TEXT,
                tags        TEXT    DEFAULT '[]',
                processed   INTEGER DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS generated (
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id             INTEGER NOT NULL REFERENCES items(id) ON DELETE CASCADE,
                type                TEXT    NOT NULL,
                content             TEXT    NOT NULL,
                fact_check_score    INTEGER,
                fact_check_sources  TEXT    DEFAULT '[]',
                created_at          TEXT    NOT NULL
            );

            CREATE TABLE IF NOT EXISTS published (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                generated_id INTEGER NOT NULL REFERENCES generated(id) ON DELETE CASCADE,
                channel      TEXT    NOT NULL,
                status       TEXT    NOT NULL DEFAULT 'draft',
                published_at TEXT
            );

            CREATE INDEX IF NOT EXISTS idx_items_fetched ON items(fetched_at DESC);
            CREATE INDEX IF NOT EXISTS idx_items_source  ON items(source);
            CREATE INDEX IF NOT EXISTS idx_items_processed ON items(processed);
        """)


# ── Items ─────────────────────────────────────────────────────────────────────

def upsert_item(url: str, title: str, source: str,
                published_at: str = None, content: str = None,
                summary: str = None, tags: list = None) -> int | None:
    """Vloží novou položku nebo přeskočí duplicate. Vrátí id nebo None."""
    import hashlib
    url_hash = hashlib.sha256(url.encode()).hexdigest()[:32]
    fetched_at = datetime.now().isoformat()
    with get_db() as conn:
        try:
            cur = conn.execute(
                """INSERT INTO items (url, url_hash, title, source, published_at,
                                     fetched_at, content, summary, tags)
                   VALUES (?,?,?,?,?,?,?,?,?)""",
                (url, url_hash, title, source, published_at,
                 fetched_at, content, summary, json.dumps(tags or []))
            )
            return cur.lastrowid
        except sqlite3.IntegrityError:
            return None  # duplicate


def get_items(limit: int = 50, offset: int = 0,
              source: str = None, processed: int = None,
              tag: str = None) -> list[dict]:
    with get_db() as conn:
        q = "SELECT * FROM items WHERE 1=1"
        params = []
        if source:
            q += " AND source = ?"; params.append(source)
        if processed is not None:
            q += " AND processed = ?"; params.append(processed)
        if tag:
            q += ' AND tags LIKE ?'; params.append(f'%"{tag}"%')
        q += " ORDER BY COALESCE(published_at, fetched_at) DESC LIMIT ? OFFSET ?"
        params += [limit, offset]
        rows = conn.execute(q, params).fetchall()
        return [dict(r) for r in rows]


def get_item(item_id: int) -> dict | None:
    with get_db() as conn:
        row = conn.execute("SELECT * FROM items WHERE id=?", (item_id,)).fetchone()
        return dict(row) if row else None


def mark_processed(item_id: int):
    with get_db() as conn:
        conn.execute("UPDATE items SET processed=1 WHERE id=?", (item_id,))


def count_items() -> dict:
    with get_db() as conn:
        total = conn.execute("SELECT COUNT(*) FROM items").fetchone()[0]
        new   = conn.execute("SELECT COUNT(*) FROM items WHERE processed=0").fetchone()[0]
        return {"total": total, "new": new}


# ── Generated ─────────────────────────────────────────────────────────────────

def save_generated(item_id: int, type: str, content: str,
                   fact_check_score: int = None,
                   fact_check_sources: list = None) -> int:
    with get_db() as conn:
        cur = conn.execute(
            """INSERT INTO generated (item_id, type, content, fact_check_score,
                                     fact_check_sources, created_at)
               VALUES (?,?,?,?,?,?)""",
            (item_id, type, content, fact_check_score,
             json.dumps(fact_check_sources or []),
             datetime.now().isoformat())
        )
        return cur.lastrowid


def get_generated(item_id: int) -> list[dict]:
    with get_db() as conn:
        rows = conn.execute("""
            SELECT g.*,
                   p.status      AS pub_status,
                   p.channel     AS pub_channel,
                   p.published_at AS pub_at
            FROM generated g
            LEFT JOIN published p ON p.generated_id = g.id AND p.status = 'published'
            WHERE g.item_id = ?
            ORDER BY g.created_at DESC
        """, (item_id,)).fetchall()
        return [dict(r) for r in rows]


def update_generated_content(gen_id: int, content: str):
    with get_db() as conn:
        conn.execute("UPDATE generated SET content=? WHERE id=?", (content, gen_id))


def get_all_generated(limit: int = 50, offset: int = 0,
                       type_filter: str = None) -> list[dict]:
    with get_db() as conn:
        q = """
            SELECT g.id, g.item_id, g.type, g.content, g.created_at,
                   i.title AS item_title, i.url AS item_url, i.source AS item_source,
                   p.channel AS published_channel,
                   p.status  AS published_status,
                   p.published_at AS published_at_ts
            FROM generated g
            JOIN items i ON g.item_id = i.id
            LEFT JOIN published p ON p.generated_id = g.id AND p.status = 'published'
        """
        params = []
        if type_filter:
            q += " WHERE g.type = ?"
            params.append(type_filter)
        q += " ORDER BY g.created_at DESC LIMIT ? OFFSET ?"
        params += [limit, offset]
        rows = conn.execute(q, params).fetchall()
        return [dict(r) for r in rows]


def count_generated() -> dict:
    with get_db() as conn:
        total = conn.execute("SELECT COUNT(*) FROM generated").fetchone()[0]
        rows  = conn.execute(
            "SELECT type, COUNT(*) as cnt FROM generated GROUP BY type"
        ).fetchall()
        return {"total": total, "by_type": {r["type"]: r["cnt"] for r in rows}}


# ── Published ─────────────────────────────────────────────────────────────────

def save_published(generated_id: int, channel: str,
                   status: str = "draft") -> int:
    with get_db() as conn:
        cur = conn.execute(
            "INSERT INTO published (generated_id, channel, status) VALUES (?,?,?)",
            (generated_id, channel, status)
        )
        return cur.lastrowid


if __name__ == "__main__":
    init_db()
    print(f"✅ Databáze inicializována: {DB_PATH}")
