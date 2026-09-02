-- Query 1: 01 High Risk Transactions
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

-- Query 2: 02 Distinct Payment Methods
SELECT DISTINCT
    payment_method
FROM transactions
ORDER BY payment_method;

-- Query 3: 03 Merchant Activity
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

-- Query 4: 04 Chargeback Impact
SELECT
    COUNT(*) AS chargeback_transactions,
    COUNT(DISTINCT user_id) AS unique_users_affected,
    SUM(amount_inr) AS total_chargeback_amount_inr
FROM transactions
WHERE status = 'chargeback';

-- Query 5: 05 Burner Accounts
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

-- Query 6: 06 Velocity Attacks
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

-- Query 7: 07 All Merchants Left Join
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

