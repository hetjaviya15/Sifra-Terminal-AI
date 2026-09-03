"""
database/database.py - SQLite database manager for SIFRA.

Handles:
  - Initialising the database and tables on first run
  - Saving and loading conversations and messages
  - Saving, reading, and deleting memories
"""

import sqlite3
import os
from datetime import datetime


from config import DB_PATH


def get_connection() -> sqlite3.Connection:
    """Open and return a SQLite database connection with row factory."""
    # Ensure the database directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Allows dict-like access to rows
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    """
    Create database tables if they don't already exist.
    This is safe to call on every startup.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # ── Conversations table ──────────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
        )
    """)

    # ── Messages table ───────────────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER NOT NULL,
            role            TEXT    NOT NULL,   -- 'user' or 'assistant'
            content         TEXT    NOT NULL,
            timestamp       TEXT    NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (conversation_id) REFERENCES conversations(id)
        )
    """)

    # ── Memories table ───────────────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            memory_key   TEXT    NOT NULL UNIQUE,
            memory_value TEXT    NOT NULL,
            created_at   TEXT    NOT NULL DEFAULT (datetime('now'))
        )
    """)

    conn.commit()
    conn.close()


# ════════════════════════════════════════════════════════════════════════════
# Conversation & Message helpers
# ════════════════════════════════════════════════════════════════════════════

def create_conversation() -> int:
    """Create a new conversation record and return its ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO conversations (created_at) VALUES (?)",
        (datetime.now().isoformat(),)
    )
    conv_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return int(conv_id) if conv_id is not None else 0


def save_message(conversation_id: int, role: str, content: str) -> None:
    """
    Persist a single message to the database.

    Args:
        conversation_id: The active conversation ID.
        role:            'user' or 'assistant'.
        content:         The message text.
    """
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO messages (conversation_id, role, content, timestamp)
        VALUES (?, ?, ?, ?)
        """,
        (conversation_id, role, content, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def get_recent_conversations(limit: int = 10) -> list[dict]:
    """
    Return the most recent conversations with their message counts.

    Args:
        limit: Maximum number of conversations to return.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            c.id,
            c.created_at,
            COUNT(m.id) AS message_count
        FROM conversations c
        LEFT JOIN messages m ON m.conversation_id = c.id
        GROUP BY c.id
        ORDER BY c.created_at DESC
        LIMIT ?
    """, (limit,))
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def get_messages_for_conversation(conversation_id: int) -> list[dict]:
    """
    Return all messages for a given conversation, oldest first.

    Args:
        conversation_id: The conversation to fetch.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT role, content, timestamp
        FROM messages
        WHERE conversation_id = ?
        ORDER BY timestamp ASC
    """, (conversation_id,))
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


# ════════════════════════════════════════════════════════════════════════════
# Memory helpers
# ════════════════════════════════════════════════════════════════════════════

def save_memory(key: str, value: str) -> None:
    """
    Save or update a memory entry (upsert).

    Args:
        key:   A short identifier, e.g. 'name' or 'favourite_language'.
        value: The value to remember.
    """
    conn = get_connection()
    conn.execute("""
        INSERT INTO memories (memory_key, memory_value, created_at)
        VALUES (?, ?, ?)
        ON CONFLICT(memory_key) DO UPDATE SET
            memory_value = excluded.memory_value,
            created_at   = excluded.created_at
    """, (key.lower().strip(), value.strip(), datetime.now().isoformat()))
    conn.commit()
    conn.close()


def get_all_memories() -> list[dict]:
    """Return all stored memories."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT memory_key, memory_value, created_at FROM memories ORDER BY created_at ASC")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def delete_memory(key: str) -> bool:
    """
    Delete a memory by key.

    Returns:
        True if a row was deleted, False if the key wasn't found.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM memories WHERE memory_key = ?", (key.lower().strip(),))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted


def clear_all_memories() -> int:
    """
    Delete all stored memories.

    Returns:
        Number of deleted memory entries.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM memories")
    count = cursor.rowcount
    conn.commit()
    conn.close()
    return count


def get_memory_context_string() -> str:
    """
    Build a compact string of all memories to inject into the AI context.
    Returns an empty string if there are no memories saved.
    """
    memories = get_all_memories()
    if not memories:
        return ""
    lines = ["[User memories]"]
    for m in memories:
        lines.append(f"- {m['memory_key']}: {m['memory_value']}")
    return "\n".join(lines)
