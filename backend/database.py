import sqlite3
from typing import List, Dict

DB_PATH = "cyberbullying.db"
_conn = sqlite3.connect(DB_PATH, check_same_thread=False)
_cursor = _conn.cursor()

_cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    message TEXT,
    timestamp TEXT,
    risk_score REAL
)
""")
_conn.commit()

def log_message(user_id: str, message: str, timestamp: str, risk_score: float):
    _cursor.execute("""
        INSERT INTO logs (user_id, message, timestamp, risk_score)
        VALUES (?, ?, ?, ?)
    """, (user_id, message, timestamp, float(risk_score)))
    _conn.commit()

def fetch_flagged_messages(limit: int = 200, min_risk: float = 0.0) -> List[Dict]:
    _cursor.execute("""
        SELECT user_id, message, timestamp, risk_score
        FROM logs
        WHERE risk_score >= ?
        ORDER BY id DESC
        LIMIT ?
    """, (min_risk, limit))
    rows = _cursor.fetchall()
    return [
        {"user_id": r[0], "message": r[1], "timestamp": r[2], "risk_score": float(r[3])}
        for r in rows
    ]
