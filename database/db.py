import calendar
import sqlite3
from datetime import date
from pathlib import Path

from werkzeug.security import generate_password_hash

# ------------------------------------------------------------------ #
# Configuration                                                       #
# ------------------------------------------------------------------ #

DB_PATH = Path(__file__).resolve().parent.parent / "expense_tracker.db"

CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now'))
)
"""

CREATE_EXPENSES_TABLE = """
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    date TEXT NOT NULL,
    description TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users (id)
)
"""


# ------------------------------------------------------------------ #
# Connection                                                          #
# ------------------------------------------------------------------ #

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ------------------------------------------------------------------ #
# Schema                                                               #
# ------------------------------------------------------------------ #

def init_db():
    conn = get_db()
    try:
        conn.execute(CREATE_USERS_TABLE)
        conn.execute(CREATE_EXPENSES_TABLE)
        conn.commit()
    finally:
        conn.close()


# ------------------------------------------------------------------ #
# Seed data                                                            #
# ------------------------------------------------------------------ #

def seed_db():
    conn = get_db()
    try:
        row = conn.execute("SELECT COUNT(*) AS count FROM users").fetchone()
        if row["count"] > 0:
            return

        password_hash = generate_password_hash("demo123")
        cursor = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            ("Demo User", "demo@spendly.com", password_hash),
        )
        user_id = cursor.lastrowid

        today = date.today()
        year, month = today.year, today.month
        days_in_month = calendar.monthrange(year, month)[1]

        # (category, amount in PKR, description, day-of-month offset)
        sample_expenses = [
            ("Food", 850.0, "Grocery shopping", 2),
            ("Transport", 300.0, "Fuel for bike", 5),
            ("Bills", 4500.0, "Electricity bill", 8),
            ("Health", 1200.0, "Pharmacy - medicines", 11),
            ("Entertainment", 650.0, "Movie tickets", 14),
            ("Shopping", 3200.0, "New shoes", 18),
            ("Food", 420.0, "Lunch with friends", 22),
            ("Other", 500.0, "Miscellaneous expense", 26),
        ]

        for category, amount, description, day_offset in sample_expenses:
            day = min(day_offset, days_in_month)
            expense_date = f"{year:04d}-{month:02d}-{day:02d}"
            conn.execute(
                """
                INSERT INTO expenses (user_id, amount, category, date, description)
                VALUES (?, ?, ?, ?, ?)
                """,
                (user_id, amount, category, expense_date, description),
            )

        conn.commit()
    finally:
        conn.close()
