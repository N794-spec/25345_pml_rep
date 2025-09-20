# backend_fin.py
import psycopg2
import pandas as pd
import os

# --- Database Connection ---
# It's best practice to use environment variables for connection details.
# Example: os.environ.get('DB_NAME')
DB_CONFIG = {
    "dbname": "pml",
    "user": "postgres",
    "password": "NAVEEN2302",
    "host": "localhost",
    "port": "5432"
}

def get_db_connection():
    """Establishes and returns a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.OperationalError as e:
        # A more robust application would have logging here.
        print(f"🔴 Could not connect to the database: {e}")
        return None

def init_db():
    """Initializes the database by creating the necessary tables if they don't exist."""
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            # You can read the SQL from the .sql file for better separation
            with open('table_creation.sql', 'r') as f:
                cur.execute(f.read())
        conn.commit()
        conn.close()
        print("Database initialized successfully.")

# --- CRUD Operations ---

# CREATE
def add_transaction(date, description, category, amount, transaction_type):
    """
    Adds a new financial transaction to the database.
    Ref: PostgreSQL Docs, Chapter: DML - INSERT
    """
    sql = """
        INSERT INTO transactions (transaction_date, description, category, amount, transaction_type)
        VALUES (%s, %s, %s, %s, %s);
    """
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute(sql, (date, description, category, amount, transaction_type))
        conn.commit()
        conn.close()

# READ
def get_all_transactions():
    """
    Retrieves all transactions and returns them as a Pandas DataFrame.
    DataFrame is ideal for BI and frontend display.
    Ref: PostgreSQL Docs, Chapter: Queries - SELECT
    """
    sql = "SELECT id, transaction_date, description, category, amount, transaction_type FROM transactions ORDER BY transaction_date DESC;"
    conn = get_db_connection()
    if conn:
        df = pd.read_sql(sql, conn)
        conn.close()
        return df
    return pd.DataFrame() # Return empty DataFrame on connection failure

# UPDATE (Example - can be extended in the frontend)
def update_transaction(transaction_id, new_amount):
    """
    Updates the amount of a specific transaction.
    Ref: PostgreSQL Docs, Chapter: DML - UPDATE
    """
    sql = "UPDATE transactions SET amount = %s WHERE id = %s;"
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute(sql, (new_amount, transaction_id))
        conn.commit()
        conn.close()

# DELETE
def delete_transaction(transaction_id):
    """
    Deletes a transaction from the database by its ID.
    Ref: PostgreSQL Docs, Chapter: DML - DELETE
    """
    sql = "DELETE FROM transactions WHERE id = %s;"
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute(sql, (transaction_id,))
        conn.commit()
        conn.close()

# --- Business Intelligence & Data Warehousing Section ---

def get_business_insights():
    """
    Calculates key business intelligence metrics using SQL aggregate functions.
    This is a core concept in data warehousing.
    Ref: PostgreSQL Docs, Chapter: Aggregate Functions
    """
    query = """
    SELECT
        COUNT(*) AS total_transactions,
        SUM(CASE WHEN transaction_type = 'Income' THEN amount ELSE 0 END) AS total_income,
        SUM(CASE WHEN transaction_type = 'Expense' THEN amount ELSE 0 END) AS total_expense,
        AVG(amount) AS average_transaction_amount,
        MAX(amount) AS max_transaction_amount,
        MIN(amount) AS min_transaction_amount
    FROM
        transactions;
    """
    conn = get_db_connection()
    if conn:
        insights = pd.read_sql(query, conn).iloc[0].to_dict()
        conn.close()
        # Calculate net savings in Python for clarity
        insights['net_savings'] = insights['total_income'] - insights['total_expense']
        return insights
    # Return a default dictionary if the connection fails
    return {
        'total_transactions': 0, 'total_income': 0, 'total_expense': 0,
        'average_transaction_amount': 0, 'max_transaction_amount': 0,
        'min_transaction_amount': 0, 'net_savings': 0
    }