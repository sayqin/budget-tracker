import sqlite3

# Connect to the existing database
conn = sqlite3.connect("budget_tracker.db")
cursor = conn.cursor()

# Example 1: Show all transactions for a user
print("\n🔍 Transactions for Alice:")
cursor.execute("""
SELECT t.date, c.name AS category, t.amount, t.description
FROM transactions t
JOIN accounts a ON t.account_id = a.id
JOIN categories c ON t.category_id = c.id
JOIN users u ON a.user_id = u.id
WHERE u.name = 'Alice'
ORDER BY t.date;
""")
for row in cursor.fetchall():
    print(row)

# Example 2: Show total expenses by category for May 2025
print("\n Alice's total expenses by category in May 2025:")
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
for row in cursor.fetchall():
    print(row)

# Example 3: Show budget vs actual spending
print("\n Budget vs Actual for May 2025:")
cursor.execute("""
SELECT c.name,
       b.limit_amount AS budget_limit,
       ROUND(COALESCE(SUM(-t.amount), 0), 2) AS actual_spent
FROM budgets b
JOIN categories c ON b.category_id = c.id
LEFT JOIN transactions t ON t.category_id = c.id
    AND strftime('%Y-%m', t.date) = b.month
    AND t.account_id IN (
        SELECT id FROM accounts WHERE user_id = b.user_id
    )
WHERE b.user_id = 1 AND b.month = '2025-05'
GROUP BY c.name, b.limit_amount;
""")
for row in cursor.fetchall():
    print(row)

conn.close()
