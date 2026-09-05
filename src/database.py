import sqlite3


def init_db(db_path="credit_card_bot.db"):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS shops (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            mcc_code TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn


def add_shop(conn, name, mcc_code):
    conn.execute(
        "INSERT OR REPLACE INTO shops (name, mcc_code) VALUES (?, ?)",
        (name, mcc_code)
    )
    conn.commit()


def delete_shop(conn, name):
    cursor = conn.execute("DELETE FROM shops WHERE name = ?", (name,))
    conn.commit()
    return cursor.rowcount > 0


def get_shop_mcc(conn, name):
    row = conn.execute(
        "SELECT mcc_code FROM shops WHERE name = ?", (name,)
    ).fetchone()
    return row["mcc_code"] if row else None


def get_all_shops(conn):
    rows = conn.execute("SELECT name, mcc_code FROM shops").fetchall()
    return [dict(row) for row in rows]
