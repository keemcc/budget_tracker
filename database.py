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

    cursor.execute("SELECT COUNT(*) FROM allowance WHERE date = ?", (date,))
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
        INSERT INTO allowance (date, allowance)
        VALUES (?, ?)
        """, (date, allowance))
    
    connector.commit()
    connector.close()

#Retrieves the total amount spent on a certain date
def get_balance_on_date(date):
    connector = sqlite3.connect(DATABASE_FILE)
    cursor = connector.cursor()
    cursor.execute("""
    SELECT
        SUM(amount) AS daily_balance
    FROM transactions
    WHERE date = ?""", (date,))

    return cursor.fetchone()[0]

#Sets the database file path
def set_database_file_path(path):
    global DATABASE_FILE
    DATABASE_FILE = path

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
def get_allowance_on_date(date):
    connector = sqlite3.connect(DATABASE_FILE)
    cursor = connector.cursor()

    cursor.execute("""
    SELECT allowance FROM allowance
    WHERE date = ?
    """, (date,))

    result = cursor.fetchone()
    if result:
        return result[0]
    return result

#Prints all transactions along with the allowance their date was given
def print_transactions_with_allowance():
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

def add_filler_data():
    add_transaction("2025-01-13", "Panda Express", "Food", 12.42, 20.00)
    add_transaction("2025-01-14", "Uber Ride", "Transportation", 8.50, 20.00)
    add_transaction("2025-01-14", "Starbucks", "Coffee", 5.75, 20.00)
    add_transaction("2025-01-15", "Amazon", "Books", 25.99, 20.00)
    add_transaction("2025-01-16", "Walmart", "Groceries", 30.20, 20.00)
    add_transaction("2025-01-17", "Movie Tickets", "Entertainment", 15.00, 20.00)
    add_transaction("2025-01-18", "McDonald's", "Food", 7.30, 20.00)
    add_transaction("2025-01-19", "Target", "Clothing", 40.15, 20.00)
    add_transaction("2025-01-20", "CVS", "Medicine", 10.95, 20.00)
    add_transaction("2025-01-21", "Whole Foods", "Groceries", 50.00, 20.00)

#Tests various functions of the database
def test():
    initalize_database()
    print_transactions_with_allowance()


test()