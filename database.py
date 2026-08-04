import sqlite3
import time
from config import DB_PATH, START_MONEY, START_EXP, START_LEVEL

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            rp_name TEXT,
            level INTEGER DEFAULT 1,
            exp INTEGER DEFAULT 0,
            money INTEGER DEFAULT 10000,
            bank_money INTEGER DEFAULT 0,
            car TEXT DEFAULT 'Отсутствует',
            faction TEXT DEFAULT 'Гражданский',
            last_work_time INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def get_player(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM players WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "user_id": row[0],
            "username": row[1],
            "rp_name": row[2],
            "level": row[3],
            "exp": row[4],
            "money": row[5],
            "bank_money": row[6],
            "car": row[7],
            "faction": row[8],
            "last_work_time": row[9]
        }
    return None

def register_player(user_id, username, rp_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO players (user_id, username, rp_name, level, exp, money, bank_money, car, faction, last_work_time)
        VALUES (?, ?, ?, ?, ?, ?, 0, 'Отсутствует', 'Гражданский', 0)
    """, (user_id, username, rp_name, START_LEVEL, START_EXP, START_MONEY))
    conn.commit()
    conn.close()

def update_player(user_id, **kwargs):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    keys = list(kwargs.keys())
    values = list(kwargs.values())
    set_clause = ", ".join([f"{key} = ?" for key in keys])
    query = f"UPDATE players SET {set_clause} WHERE user_id = ?"
    cursor.execute(query, values + [user_id])
    conn.commit()
    conn.close()
