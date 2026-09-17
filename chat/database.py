import sqlite3
from pathlib import Path

from chat.config import MAX_SESSIONS, MAX_TURNS_PER_SESSION

DB_PATH = Path("chat_history.db")
MAX_ROWS_PER_SESSION = MAX_TURNS_PER_SESSION * 2


def _connect():
    return sqlite3.connect(DB_PATH)


def init_database():
    conn = _connect()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_id INTEGER NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(conversation_id) REFERENCES conversations(id)
    )
    """)

    conn.commit()
    conn.close()


def create_conversation(name):
    conn = _connect()
    c = conn.cursor()
    c.execute("INSERT INTO conversations (name) VALUES (?)", (name,))
    conversation_id = c.lastrowid
    conn.commit()
    conn.close()

    trim_sessions()
    return conversation_id


def get_conversations():
    # (id, name, created_at, updated_at, 메시지 행 수)
    conn = _connect()
    c = conn.cursor()
    c.execute("""
    SELECT c.id, c.name, c.created_at, c.updated_at, COUNT(m.id)
    FROM conversations c
    LEFT JOIN messages m ON m.conversation_id = c.id
    GROUP BY c.id
    ORDER BY c.updated_at DESC, c.id DESC
    """)
    rows = c.fetchall()
    conn.close()
    return rows


def get_conversation_messages(conversation_id):
    # created_at은 초 단위라 같은 초에 저장된 행끼리 순서가 뒤집힌다. id로 정렬해야 안전하다.
    conn = _connect()
    c = conn.cursor()
    c.execute("""
    SELECT role, content, created_at
    FROM messages WHERE conversation_id = ? ORDER BY id ASC
    """, (conversation_id,))
    rows = c.fetchall()
    conn.close()
    return rows


def save_turn(conversation_id, user_content, assistant_content):
    # 한 턴을 함께 저장해야 트리밍 시 user/assistant 짝이 깨지지 않는다.
    conn = _connect()
    c = conn.cursor()
    c.executemany(
        "INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
        [
            (conversation_id, "user", user_content),
            (conversation_id, "assistant", assistant_content),
        ],
    )
    c.execute(
        "UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (conversation_id,),
    )
    conn.commit()
    conn.close()

    trim_messages(conversation_id)


def trim_messages(conversation_id):
    # 세션당 MAX_TURNS_PER_SESSION턴만 남기고 오래된 턴부터 삭제
    conn = _connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM messages WHERE conversation_id = ?", (conversation_id,))
    excess = c.fetchone()[0] - MAX_ROWS_PER_SESSION

    if excess > 0:
        c.execute("""
        DELETE FROM messages WHERE id IN (
            SELECT id FROM messages WHERE conversation_id = ? ORDER BY id ASC LIMIT ?
        )
        """, (conversation_id, excess))
        conn.commit()

    conn.close()


def trim_sessions():
    # 최근 사용순 MAX_SESSIONS개만 남기고 오래된 세션부터 삭제
    conn = _connect()
    c = conn.cursor()
    c.execute(
        "SELECT id FROM conversations ORDER BY updated_at DESC, id DESC LIMIT -1 OFFSET ?",
        (MAX_SESSIONS,),
    )
    old_ids = [row[0] for row in c.fetchall()]

    if old_ids:
        placeholders = ",".join("?" * len(old_ids))
        # FK CASCADE가 없으므로 자식 행을 먼저 지워야 고아 행이 남지 않는다.
        c.execute(f"DELETE FROM messages WHERE conversation_id IN ({placeholders})", old_ids)
        c.execute(f"DELETE FROM conversations WHERE id IN ({placeholders})", old_ids)
        conn.commit()

    conn.close()


def delete_conversation(conversation_id):
    conn = _connect()
    c = conn.cursor()
    c.execute("DELETE FROM messages WHERE conversation_id = ?", (conversation_id,))
    c.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
    conn.commit()
    conn.close()
