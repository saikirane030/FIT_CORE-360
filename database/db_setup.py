import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "fitcore360.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    c = conn.cursor()

    # Users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            weight REAL,
            height REAL,
            goal TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Diet history table
    c.execute("""
        CREATE TABLE IF NOT EXISTS diet_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT,
            meal TEXT,
            food_item TEXT,
            calories REAL,
            protein REAL,
            carbs REAL,
            fat REAL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # Weight tracking table
    c.execute("""
        CREATE TABLE IF NOT EXISTS weight_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT,
            weight REAL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()

def save_user(name, age, gender, weight, height, goal):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO users (name, age, gender, weight, height, goal)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, age, gender, weight, height, goal))
    user_id = c.lastrowid
    conn.commit()
    conn.close()
    return user_id

def get_all_users():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users ORDER BY created_at DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def save_diet_entry(user_id, date, meal, food_item, calories, protein, carbs, fat):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO diet_history (user_id, date, meal, food_item, calories, protein, carbs, fat)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, date, meal, food_item, calories, protein, carbs, fat))
    conn.commit()
    conn.close()

def get_diet_history(user_id):
    conn = get_connection()
    import pandas as pd
    df = pd.read_sql_query(
        "SELECT * FROM diet_history WHERE user_id=? ORDER BY date DESC",
        conn, params=(user_id,)
    )
    conn.close()
    return df


def delete_diet_entry(entry_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM diet_history WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()


def save_weight_log(user_id, date, weight):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO weight_log (user_id, date, weight) VALUES (?, ?, ?)",
              (user_id, date, weight))
    conn.commit()
    conn.close()

def get_weight_log(user_id):
    conn = get_connection()
    import pandas as pd
    df = pd.read_sql_query(
        "SELECT * FROM weight_log WHERE user_id=? ORDER BY date ASC",
        conn, params=(user_id,)
    )
    conn.close()
    return df


def delete_user(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id = ?", (user_id,))
    c.execute("DELETE FROM diet_history WHERE user_id = ?", (user_id,))
    c.execute("DELETE FROM weight_log WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
