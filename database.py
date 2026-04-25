import sqlite3
import pandas as pd

DB_NAME = 'expense.db'

def get_connection():
    # Helper function to get a SQLite database connection
    return sqlite3.connect(DB_NAME)

def create_tables():
    """Create the necessary database tables if they do not exist."""
    conn = get_connection()
    c = conn.cursor()
    # Create Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    # Create Settings table
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_settings (
            username TEXT PRIMARY KEY,
            budget REAL DEFAULT 10000,
            FOREIGN KEY (username) REFERENCES users(username)
        )
    ''')
    # Create Expenses table
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            day INTEGER NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            image BLOB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (username) REFERENCES users(username)
        )
    ''')
    
    # Migration: Add image column 
    try:
        c.execute("ALTER TABLE expenses ADD COLUMN image BLOB")
    except sqlite3.OperationalError:
        pass

    # Migration: Add created_at column
    try:
        c.execute("ALTER TABLE expenses ADD COLUMN created_at TIMESTAMP DEFAULT '2024-01-01 00:00:00'")
    except sqlite3.OperationalError:
        pass

    conn.commit()
    conn.close()

def get_budget(username):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT budget FROM user_settings WHERE username = ?', (username,))
    row = c.fetchone()
    conn.close()
    return float(row[0]) if row else 10000.0

def update_budget(username, budget):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO user_settings (username, budget) VALUES (?, ?) ON CONFLICT(username) DO UPDATE SET budget = ?', (username, budget, budget))
    conn.commit()
    conn.close()

def add_user(username, password):
    """Add a new user to the database. Returns True if successful, False if user exists."""
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # User already exists
        return False
    finally:
        conn.close()

def login_user(username, password):
    """Check if the provided username and password match any user in the database."""
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    data = c.fetchone()
    conn.close()
    return data is not None

def add_expense(username, day, category, amount, image=None):
    """Insert a new expense record for a specific user."""
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        'INSERT INTO expenses (username, day, category, amount, image) VALUES (?, ?, ?, ?, ?)',
        (username, day, category, amount, image)
    )
    conn.commit()
    conn.close()

def get_user_expenses(username):
    """Fetch all expenses for a specific user and return them as a Pandas DataFrame."""
    conn = get_connection()
    df = pd.read_sql_query('SELECT id, day, category, amount, image, created_at FROM expenses WHERE username = ? ORDER BY created_at ASC', conn, params=(username,))
    conn.close()
    return df

def delete_expense(expense_id, username):
    """Delete a specific expense for a user."""
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM expenses WHERE id = ? AND username = ?', (expense_id, username))
    conn.commit()
    conn.close()

def update_expense(expense_id, username, category, amount, image=None):
    """Update a specific expense for a user."""
    conn = get_connection()
    c = conn.cursor()
    if image is not None:
        c.execute(
            'UPDATE expenses SET category = ?, amount = ?, image = ? WHERE id = ? AND username = ?',
            (category, amount, image, expense_id, username)
        )
    else:
        c.execute(
            'UPDATE expenses SET category = ?, amount = ? WHERE id = ? AND username = ?',
            (category, amount, expense_id, username)
        )
    conn.commit()
    conn.close()

def change_password(username, new_password):
    """Update user's password."""
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE users SET password = ? WHERE username = ?', (new_password, username))
    conn.commit()
    conn.close()

def reset_user_data(username):
    """Delete all expenses for a specific user."""
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM expenses WHERE username = ?', (username,))
    conn.commit()
    conn.close()

def update_username(old_username, new_username):
    """Safely updates a user's username."""
    conn = get_connection()
    c = conn.cursor()
    try:
        # Check if new username exists
        c.execute('SELECT username FROM users WHERE username = ?', (new_username,))
        if c.fetchone():
            return False # already taken

        c.execute('UPDATE users SET username = ? WHERE username = ?', (new_username, old_username))
        c.execute('UPDATE expenses SET username = ? WHERE username = ?', (new_username, old_username))
        conn.commit()
        return True
    except Exception as e:
        return False
    finally:
        conn.close()
