
from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "paytm_payments.db"

# Recreate database cleanly whenever this script is run
if DB_PATH.exists():
    DB_PATH.unlink()

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON;")

conn.executescript("""
CREATE TABLE merchants (
    merchant_id INTEGER PRIMARY KEY,
    merchant_name TEXT NOT NULL,
    category TEXT NOT NULL,
    region TEXT NOT NULL
);

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    signup_date TEXT NOT NULL
);

CREATE TABLE transactions (
    transaction_id TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL,
    merchant_id INTEGER NOT NULL,
    transaction_time TEXT NOT NULL,
    amount_inr REAL NOT NULL,
    payment_method TEXT NOT NULL,
    status TEXT NOT NULL,
    risk_score INTEGER NOT NULL,

    FOREIGN KEY (user_id)
        REFERENCES users(user_id),

    FOREIGN KEY (merchant_id)
        REFERENCES merchants(merchant_id)
);
""")

merchants = pd.read_csv(BASE_DIR / "merchants.csv")
users = pd.read_csv(BASE_DIR / "users.csv")
transactions = pd.read_csv(BASE_DIR / "ledger.csv")

merchants.to_sql(
    "merchants",
    conn,
    if_exists="append",
    index=False
)

users.to_sql(
    "users",
    conn,
    if_exists="append",
    index=False
)

transactions.to_sql(
    "transactions",
    conn,
    if_exists="append",
    index=False
)

conn.commit()

print("Database created:", DB_PATH)
print("Merchants:", pd.read_sql_query(
    "SELECT COUNT(*) AS n FROM merchants", conn
)["n"][0])

print("Users:", pd.read_sql_query(
    "SELECT COUNT(*) AS n FROM users", conn
)["n"][0])

print("Transactions:", pd.read_sql_query(
    "SELECT COUNT(*) AS n FROM transactions", conn
)["n"][0])

foreign_key_errors = conn.execute(
    "PRAGMA foreign_key_check;"
).fetchall()

print("Foreign-key errors:", len(foreign_key_errors))

conn.close()
