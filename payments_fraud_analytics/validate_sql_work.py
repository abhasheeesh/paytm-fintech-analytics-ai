
from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent

db = sqlite3.connect(
    BASE_DIR / "paytm_payments.db"
)

merchant_count = pd.read_sql_query(
    "SELECT COUNT(*) AS n FROM merchants",
    db
)["n"][0]

user_count = pd.read_sql_query(
    "SELECT COUNT(*) AS n FROM users",
    db
)["n"][0]

txn_count = pd.read_sql_query(
    "SELECT COUNT(*) AS n FROM transactions",
    db
)["n"][0]

fk_errors = db.execute(
    "PRAGMA foreign_key_check;"
).fetchall()

db.close()

burners = pd.read_csv(
    BASE_DIR /
    "sql_outputs/05_burner_accounts.csv"
)

velocity = pd.read_csv(
    BASE_DIR /
    "sql_outputs/06_velocity_attacks.csv"
)

assert merchant_count == 40
assert user_count == 365
assert txn_count == 547
assert len(fk_errors) == 0

assert len(burners) >= 15
assert (burners["account_age_days"] >= 0).all()
assert (burners["account_age_days"] < 30).all()

assert len(velocity) >= 8
assert (velocity["transaction_count_10min"] >= 3).all()

print("PASS — merchants table: 40")
print("PASS — users table: 365")
print("PASS — transactions table: 547")
print("PASS — foreign-key check")
print("PASS — burner-account detection:", len(burners))
print("PASS — velocity-cluster detection:", len(velocity))
print()
print("PART 1 SQL CORE ACCEPTANCE CHECKS PASSED")
