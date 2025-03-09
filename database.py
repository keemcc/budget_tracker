import sqlite3
from datetime import datetime

DATABASE_FILE = "Budget_Tracker.db"
ALLOWANCE = 24.5

#Initializes the database with option of having a different allowance
def initalize_database():
    connector = sqlite3.connect(DATABASE_FILE)
    cursor = connector.cursor()

    #Create transactions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        title TEXT,
        description TEXT,
        amount REAL
    );
    """)

    #Create allowance table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS allowance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        allowance REAL
    );               
    """)

    connector.commit()
    connector.close()

#Adds a transaction to the database
def add_transaction(date, title, description, amount, allowance):
    connector = sqlite3.connect(DATABASE_FILE)
    cursor = connector.cursor()

    cursor.execute("""
    INSERT INTO transactions (date, title, description, amount)
    VALUES (?, ?, ?, ?)
    """, (date, title, description, amount))

    cursor.execute("""
    INSERT INTO allowance (date, allowance)
    VALUES (?, ?)
    """, (date, allowance))
    
    connector.commit()
    connector.close()

#Retrieves the total amount spent on a certain date
def getBalanceOnDate(date):
    connector = sqlite3.connect(DATABASE_FILE)
    cursor = connector.cursor()
    cursor.execute("""
    SELECT
        SUM(amount) AS daily_balance
    FROM transactions
    WHERE date = ?""", (date,))

    return cursor.fetchone()[0]

###Testing Functions###
#Prints all transactions stored
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

#Retrieves the allowance on a specific date
def getAllowanceOnDate(date):
    connector = sqlite3.connect(DATABASE_FILE)
    cursor = connector.cursor()

    cursor.execute("""
    SELECT allowance FROM allowance
    WHERE date = ?
    """, (date,))

    return cursor.fetchone()[0]

def printTransactionsWithAllowance():
    connector = sqlite3.connect(DATABASE_FILE)
    cursor = connector.cursor()

    cursor.execute("""
    SELECT t.id, t.date, t.title, t.description, t.amount, allowance.allowance FROM transactions AS t
    LEFT JOIN allowance ON t.date = allowance.date
    ORDER BY t.date ASC
    """)

    transactions = cursor.fetchall()
    connector.close()

    for transaction in transactions:
        print(transaction)

#Tests various functions of the database
def test():
    initalize_database()
    add_transaction("2025-1-12", "Panda Express", "Food", 12.46, 20)
    add_transaction("2025-1-13", "Panda Express", "Food", 12.42, 15)
    add_transaction("2025-1-14", "Panda Express", "Food", 8.43, 12)
    retrieve_all_transactions()
    print(f"allowance 1 {getAllowanceOnDate("2025-1-12")}")
    print(f"allowance 2 {getAllowanceOnDate("2025-1-13")}")
    print(f"allowance 3 {getAllowanceOnDate("2025-1-14")}")
    print(f"Balance on 1-12 {getBalanceOnDate("2025-1-12")}")

test()