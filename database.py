import sqlite3
from datetime import datetime

DATABASE_FILE = "Budget_Tracker.db"
ALLOWANCE = 24.5

def initalize_database():
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

def test():
    initalize_database()
    add_transaction("2025-1-12", "Panda Express", "Food", 12.46)
    add_transaction("2025-1-13", "Panda Express", "Food", 12.42)
    add_transaction("2025-1-14", "Panda Express", "Food", 8.43)
    retrieve_all_transactions()

test()