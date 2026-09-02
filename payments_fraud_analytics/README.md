
# Part 1 — Payments & Fraud Analytics

## Overview

This module covers Paytm-style payment operations through spreadsheet merchant analysis, SQL fraud-pattern detection, payment reconciliation, and a four-layer analytics dashboard.

## Data Generation

Run:

```bash
python generate_data.py
```

from inside the `payments_fraud_analytics` directory.

The fixed seed produces:

- 40 merchants
- 365 total users after burner-account injection
- 547 ledger transactions
- 15 burner-account chargebacks
- 32 velocity-attack transactions across 8 clusters
- a deliberately discrepant gateway export

## Merchant Workbook

`merchant_workbook.xlsx` demonstrates:

- VLOOKUP with fixed absolute references
- IFERROR handling
- HLOOKUP
- nested IF/AND logic
- merchant/status pivot analysis
- transaction-count versus unique-days comparison

Illustrative payment-fee assumptions are:

- UPI: 0.00%
- Wallet: 0.50%
- Card: 1.00%
- Netbanking: 1.50%

A transaction is classified as `High-Value Merchant Day` when that merchant's total transaction value for the calendar day exceeds INR 5,000 and the merchant's region is not East.

## SQLite and Fraud Detection

`create_database.py` creates the normalized SQLite database `paytm_payments.db`.

`run_fraud_queries.py` executes seven SQL queries covering the required SQL operations.

Key findings:

- Chargeback transactions: 28
- Unique chargeback users: 27
- Total chargeback amount: INR 54,472
- Burner-account rows detected: 15
- Seeded velocity clusters detected: 8

SQL outputs are stored in `sql_outputs/`.

## Payment Reconciliation

`reconcile.py` compares the internal ledger with the gateway export.

Observed discrepancy counts are:

- Missing in gateway: 27
- Extra in gateway: 10
- Amount mismatches: 16
- Status mismatches: 9

The exact dashboard reconciliation match rate is:

`495 / 547 = 90.49%`

## Dashboard

The dashboard contains four layers:

1. Headline scorecards
2. Daily trends
3. Payment-method and merchant-category breakdowns
4. Top-10 merchant detail table

### Headline Interpretation

The platform processed total GMV of INR 382,603 across the synthetic transaction window, with a captured-payment success rate of 85.56%. The exact reconciliation match rate is 90.49%, which shows that most ledger records agree with the gateway export but a meaningful minority require reconciliation. The platform-wide chargeback ratio is 5.12%, reflecting the deliberately injected fraud cases as well as baseline chargebacks.

### Trends Interpretation

Daily GMV varies noticeably across the 30-day period, with the highest daily value reaching INR 28,284 on 11 January 2026. Chargeback activity does not perfectly move with transaction value: the highest daily chargeback count is four transactions on 23 January. This suggests that transaction volume or GMV alone would not be sufficient for monitoring fraud risk.

### Breakdown Interpretation

UPI contributes the largest GMV at INR 172,274, followed by Card at INR 102,429, making UPI the dominant payment method in the generated dataset. At the merchant-category level, ecommerce produces the highest GMV at INR 79,896, followed closely by travel and grocery. The distribution therefore shows concentration in a few payment methods and categories without all activity being dominated by a single merchant segment.

### Details Interpretation

Merchant_016 has the highest transaction count among the top merchants with 20 transactions and no chargebacks. Merchant_029 is more concerning: it has 19 transactions, of which three are chargebacks, giving a chargeback ratio of approximately 15.79%. Several other top-10 merchants also exceed the 1% chargeback threshold, demonstrating why transaction volume and merchant-level risk should be reviewed together rather than independently.

Saved dashboard outputs are stored in `dashboard_outputs/`.
