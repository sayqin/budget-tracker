import sqlite3

try:
    # Connect to the database
    conn = sqlite3.connect("budget_tracker.db")
    cursor = conn.cursor()

    # Transactions for a specific user (e.g., Alice)
    print("\nTransactions for Alice:")
    cursor.execute("""
    SELECT t.date, c.name AS category, t.amount, t.description
    FROM transactions t
    JOIN accounts a ON t.account_id = a.id
    JOIN categories c ON t.category_id = c.id
    JOIN users u ON a.user_id = u.id
    WHERE u.name = ?
    ORDER BY t.date;
    """, ('Alice',))
    transactions = cursor.fetchall()
    for row in transactions:
        print(row)

    # Total expenses by category for May 2025
    print("\nAlice's total expenses by category in May 2025:")
    cursor.execute("""
    SELECT c.name, ROUND(SUM(-t.amount), 2) AS total_spent
    FROM transactions t
    JOIN accounts a ON t.account_id = a.id
    JOIN categories c ON t.category_id = c.id
    WHERE a.user_id = 1
      AND c.type = 'Expense'
      AND strftime('%Y-%m', t.date) = '2025-05'
    GROUP BY c.name;
    """)
    expenses = cursor.fetchall()
    for row in expenses:
        print(row)

    # Budget vs Actual for May 2025
    print("\nBudget vs Actual for May 2025:")
    cursor.execute("""
    SELECT c.name,
           b.limit_amount AS budget_limit,
           ROUND(COALESCE(SUM(-t.amount), 0), 2) AS actual_spent
    FROM budgets b
    JOIN categories c ON b.category_id = c.id
    LEFT JOIN transactions t 
        ON t.category_id = c.id
        AND strftime('%Y-%m', t.date) = b.month
        AND t.account_id IN (
            SELECT id FROM accounts WHERE user_id = b.user_id
        )
    WHERE b.user_id = 1 AND b.month = '2025-05'
    GROUP BY c.name, b.limit_amount;
    """)
    budgets = cursor.fetchall()
    for row in budgets:
        print(row)

except sqlite3.Error as e:
    print(f"Database error: {e}")

finally:
    if conn:
        conn.close()
