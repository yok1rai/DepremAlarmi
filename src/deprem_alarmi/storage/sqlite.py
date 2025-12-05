import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "earthquakes.db"


def init_db():
    DATA_DIR.mkdir(exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS earthquakes (
            id TEXT PRIMARY KEY,
            place TEXT,
            magnitude REAL,
            depth REAL,
            time INTEGER
        )
        """)


def save_quake(quake: dict):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
        INSERT OR IGNORE INTO earthquakes
        (id, place, magnitude, depth, time)
        VALUES (?, ?, ?, ?, ?)
        """, (
            quake["id"],
            quake["place"],
            quake["magnitude"],
            quake["depth"],
            quake["time"]
        ))


def quake_exists(quake_id: str) -> bool:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            "SELECT 1 FROM earthquakes WHERE id = ?",
            (quake_id,)
        )
        return cur.fetchone() is not None
