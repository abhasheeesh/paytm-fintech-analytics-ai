
from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "paytm_payments.db"
OUTPUT_DIR = BASE_DIR / "sql_outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

QUERIES = {

    "01_high_risk_transactions": """
SELECT
    transaction_id,
    user_id,
    merchant_id,
    amount_inr,
    payment_method,
    status,
    risk_score
FROM transactions
WHERE risk_score >= 80
ORDER BY risk_score DESC, amount_inr DESC
LIMIT 10;
""",

    "02_distinct_payment_methods": """
SELECT DISTINCT
    payment_method
FROM transactions
ORDER BY payment_method;
""",

    "03_merchant_activity": """
SELECT
    m.merchant_id,
    m.merchant_name,
    m.category,
    COUNT(t.transaction_id) AS transaction_count,
    SUM(t.amount_inr) AS total_gmv_inr
FROM merchants AS m
INNER JOIN transactions AS t
    ON m.merchant_id = t.merchant_id
GROUP BY
    m.merchant_id,
    m.merchant_name,
    m.category
HAVING COUNT(t.transaction_id) >= 10
ORDER BY total_gmv_inr DESC;
""",

    "04_chargeback_impact": """
SELECT
    COUNT(*) AS chargeback_transactions,
    COUNT(DISTINCT user_id) AS unique_users_affected,
    SUM(amount_inr) AS total_chargeback_amount_inr
FROM transactions
WHERE status = 'chargeback';
""",

    "05_burner_accounts": """
SELECT
    t.transaction_id,
    t.user_id,
    u.signup_date,
    t.transaction_time,
    t.amount_inr,
    ROUND(
        julianday(t.transaction_time)
        - julianday(u.signup_date),
        2
    ) AS account_age_days
FROM transactions AS t
INNER JOIN users AS u
    ON t.user_id = u.user_id
WHERE
    t.status = 'chargeback'
    AND (
        julianday(t.transaction_time)
        - julianday(u.signup_date)
    ) >= 0
    AND (
        julianday(t.transaction_time)
        - julianday(u.signup_date)
    ) < 30
ORDER BY t.transaction_time;
""",

    "06_velocity_attacks": """
SELECT
    user_id,

    datetime(
        (
            CAST(strftime('%s', transaction_time) AS INTEGER)
            / 600
        ) * 600,
        'unixepoch'
    ) AS ten_minute_bucket_start,

    MIN(transaction_time)
        AS cluster_earliest_transaction_time,

    COUNT(*)
        AS transaction_count_10min

FROM transactions

GROUP BY
    user_id,
    ten_minute_bucket_start

HAVING COUNT(*) >= 3

ORDER BY
    user_id,
    ten_minute_bucket_start;
""",

    "07_all_merchants_left_join": """
SELECT
    m.merchant_id,
    m.merchant_name,
    m.region,
    COUNT(t.transaction_id) AS transaction_count,
    COALESCE(SUM(t.amount_inr), 0) AS total_gmv_inr
FROM merchants AS m
LEFT JOIN transactions AS t
    ON m.merchant_id = t.merchant_id
GROUP BY
    m.merchant_id,
    m.merchant_name,
    m.region
ORDER BY transaction_count DESC;
"""
}


def main():

    conn = sqlite3.connect(DB_PATH)

    # Save all SQL in one assessable .sql file
    sql_file = BASE_DIR / "fraud_queries.sql"

    with open(sql_file, "w", encoding="utf-8") as f:

        for number, (name, query) in enumerate(
            QUERIES.items(), start=1
        ):

            f.write(
                f"-- Query {number}: "
                f"{name.replace('_', ' ').title()}\n"
            )

            f.write(query.strip())
            f.write("\n\n")


    # Execute every query and save its output
    for name, query in QUERIES.items():

        result = pd.read_sql_query(query, conn)

        output_path = OUTPUT_DIR / f"{name}.csv"

        result.to_csv(
            output_path,
            index=False
        )

        print(
            f"{name}: "
            f"{len(result)} output row(s)"
        )

    conn.close()

    print("\nSQL queries saved to fraud_queries.sql")
    print("Outputs saved in sql_outputs/")


if __name__ == "__main__":
    main()
