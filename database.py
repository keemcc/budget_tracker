import sqlite3
from datetime import datetime

DATABASE_FILE = "Budget_Tracker.db"
ALLOWANCE = 24.5

def initalize_database(allowance = ALLOWANCE):
    sqliteConnection = sqlite3.connect(DATABASE_FILE)
    cursor = sqliteConnection.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        title TEXT,
        description TEXT,
        amount REAL
    );
    """
    cursor.execute(query)

    query = """
    CREATE TABLE IF NOT EXISTS settings (
        id INTEGER PRIMARY KEY,
        allowance REAL
    );"""
    cursor.execute(query)

    cursor.execute("SELECT COUNT(*) FROM settings")
    if (cursor.fetchone()[0] == 0):
        query = """
        INSERT INTO settings (id, allowance)
        VALUES (1, ?)
        """
        cursor.execute(query, (allowance,))
    cursor.execute("SELECT allowance FROM settings WHERE id = 1")
    if (cursor.fetchone()[0] != allowance):
        cursor.execute("""
    UPDATE settings
    SET allowance = ?
    WHERE id = 1;
    """, (allowance,))

    sqliteConnection.commit()
    sqliteConnection.close()

def add_transaction(date, title, description, amount):
    sqliteConnection = sqlite3.connect(DATABASE_FILE)
    cursor = sqliteConnection.cursor()

    query = """
    INSERT INTO transactions (date, title, description, amount)
    VALUES (?, ?, ?, ?)
    """
    cursor.execute(query, (date, title, description, amount))
    sqliteConnection.commit()
    sqliteConnection.close()



#Testing Functions
def retrieve_all_transactions():
    sqliteConnection = sqlite3.connect(DATABASE_FILE)
    cursor = sqliteConnection.cursor()

    query = """
    SELECT id, date, title, description, amount FROM transactions
    ORDER BY date ASC
    """
    cursor.execute(query)

    transactions = cursor.fetchall()
    sqliteConnection.close()

    for transaction in transactions:
        print(transaction)

def getAllowance():
    sqliteConnection = sqlite3.connect(DATABASE_FILE)
    cursor = sqliteConnection.cursor()

    query = """
    SELECT id, allowance FROM settings
    """
    cursor.execute(query)

    return cursor.fetchone()

def test():
    initalize_database(23)
    add_transaction("2025-1-12", "Panda Express", "Food", 12.46)
    add_transaction("2025-1-13", "Panda Express", "Food", 12.42)
    add_transaction("2025-1-14", "Panda Express", "Food", 8.43)
    retrieve_all_transactions()
    print(getAllowance())

test()