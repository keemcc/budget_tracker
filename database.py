import sqlite3
from datetime import datetime

DATABASE_FILE = "Budget_Tracker.db"
ALLOWANCE = 24.5

#Initializes the database with option of having a different allowance
def initalize_database(allowance = ALLOWANCE):
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

    #Create settings table to store allowance
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        id INTEGER PRIMARY KEY,
        allowance REAL
    );
    """)

    #Insert allowance if it doesn't exist
    cursor.execute("SELECT COUNT(*) FROM settings")
    if (cursor.fetchone()[0] == 0):
        cursor.execute("""
        INSERT INTO settings (id, allowance)
        VALUES (1, ?)
        """, (allowance,))
    #If it does exist, make sure it is the set allowance
    else:
        cursor.execute("SELECT allowance FROM settings WHERE id = 1")
        if (cursor.fetchone()[0] != allowance):
            cursor.execute("""
            UPDATE settings
            SET allowance = ?
            WHERE id = 1;
            """, (allowance,))

    connector.commit()
    connector.close()

#Adds a transaction to the database
def add_transaction(date, title, description, amount):
    connector = sqlite3.connect(DATABASE_FILE)
    cursor = connector.cursor()

    cursor.execute("""
    INSERT INTO transactions (date, title, description, amount)
    VALUES (?, ?, ?, ?)
    """, (date, title, description, amount))
    
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

#Retrieves the allowance stored in settings
def getAllowance():
    sqliteConnection = sqlite3.connect(DATABASE_FILE)
    cursor = sqliteConnection.cursor()

    query = """
    SELECT allowance FROM settings
    WHERE id = 1
    """
    cursor.execute(query)

    return cursor.fetchone()[0]

#Tests various functions of the database
def test():
    initalize_database(24)
    add_transaction("2025-1-12", "Panda Express", "Food", 12.46)
    add_transaction("2025-1-13", "Panda Express", "Food", 12.42)
    add_transaction("2025-1-14", "Panda Express", "Food", 8.43)
    retrieve_all_transactions()
    print(getAllowance())
    print(getBalanceOnDate("2025-1-12"))

test()