import sqlite3
import random
from datetime import datetime, timedelta

# Connect to the database
conn = sqlite3.connect('finance_tracker.db')
cursor = conn.cursor()

# Create required tables if they don't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    password TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    amount REAL,
    category TEXT,
    date TEXT,
    description TEXT,
    payment_method TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')

# Check if there's a user
cursor.execute("SELECT id FROM users LIMIT 1")
user = cursor.fetchone()

# Create user if not exists
if not user:
    cursor.execute("INSERT INTO users (username, email, phone, password) VALUES (?, ?, ?, ?)",
                  ("testuser", "test@example.com", "1234567890", "password"))
    conn.commit()
    user_id = cursor.lastrowid
    print(f"Created test user with ID: {user_id}")
else:
    user_id = user[0]
    print(f"Using existing user with ID: {user_id}")

# Dummy data
categories = ["Food", "Transportation", "Entertainment", "Utilities", "Shopping", "Health", "Education"]
payment_methods = ["Cash", "UPI", "Credit Card", "Debit Card"]
current_date = datetime.now()

# Add 10 random transactions
for i in range(10):
    amount = round(random.uniform(100, 5000), 2)
    category = random.choice(categories)
    days_ago = random.randint(0, 30)
    transaction_date = (current_date - timedelta(days=days_ago)).strftime('%Y-%m-%d')
    payment_method = random.choice(payment_methods)
    description = f"Dummy transaction #{i+1} for {category}"

    cursor.execute(
        "INSERT INTO transactions (user_id, amount, category, date, description, payment_method) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, amount, category, transaction_date, description, payment_method)
    )

    print(f"Added transaction: {amount} for {category} on {transaction_date} via {payment_method}")

conn.commit()
conn.close()
print("\nSuccessfully added 10 dummy transactions to the database.")