import sqlite3

try:
    # Connect to SQLite (creates a new file if not exists)
    conn = sqlite3.connect("budget_tracker.db")
    cursor = conn.cursor()

    # Drop tables if script is re-run
    cursor.executescript("""
    DROP TABLE IF EXISTS transactions;
    DROP TABLE IF EXISTS budgets;
    DROP TABLE IF EXISTS accounts;
    DROP TABLE IF EXISTS categories;
    DROP TABLE IF EXISTS users;
    """)

    # Create tables
    cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        balance REAL DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT CHECK(type IN ('Income', 'Expense')) NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_id INTEGER NOT NULL,
        category_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        amount REAL NOT NULL CHECK(amount != 0),
        description TEXT,
        FOREIGN KEY (account_id) REFERENCES accounts(id),
        FOREIGN KEY (category_id) REFERENCES categories(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE budgets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        category_id INTEGER NOT NULL,
        month TEXT NOT NULL,
        limit_amount REAL NOT NULL CHECK(limit_amount > 0),
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (category_id) REFERENCES categories(id),
        UNIQUE (user_id, category_id, month)
    );
    """)

    # Insert initial sample data
    cursor.executemany("INSERT INTO users (name, email) VALUES (?, ?)", [
        ('Alice', 'alice@example.com'),
        ('Bob', 'bob@example.com')
    ])

    cursor.executemany("INSERT INTO accounts (user_id, name, type, balance) VALUES (?, ?, ?, ?)", [
        (1, 'Checking Account', 'Checking', 1500.00),
        (1, 'Credit Card', 'Credit', -200.00),
        (2, 'Savings Account', 'Savings', 5000.00)
    ])

    cursor.executemany("INSERT INTO categories (name, type) VALUES (?, ?)", [
        ('Salary', 'Income'),
        ('Groceries', 'Expense'),
        ('Rent', 'Expense'),
        ('Dining Out', 'Expense')
    ])

    cursor.executemany("INSERT INTO transactions (account_id, category_id, date, amount, description) VALUES (?, ?, ?, ?, ?)", [
        (1, 1, '2025-05-01', 3000.00, 'Monthly Salary'),
        (1, 2, '2025-05-02', -150.25, 'Supermarket shopping'),
        (1, 3, '2025-05-03', -950.00, 'May Rent'),
        (2, 4, '2025-05-04', -40.00, 'Lunch with friends')
    ])

    cursor.executemany("INSERT INTO budgets (user_id, category_id, month, limit_amount) VALUES (?, ?, ?, ?)", [
        (1, 2, '2025-05', 400.00),
        (1, 3, '2025-05', 1000.00),
        (1, 4, '2025-05', 150.00)
    ])

    # Commit changes
    conn.commit()
    print("Schema and sample data created successfully.")

except sqlite3.Error as e:
    print(f"Database error: {e}")

finally:
    if conn:
        conn.close()
