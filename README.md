
# Paytm FinTech Analytics & AI Platform

## Overview

This repository contains one connected Paytm-style FinTech analytics platform covering three business areas:

1. Payments and fraud analytics
2. Credit-risk and lending machine learning
3. AI-augmented wealth advisory and blockchain/crypto risk

All monetary values in this project are expressed in Indian Rupees (INR).

## Repository Structure

```text
payments_fraud_analytics/
credit_risk_lending_ml/
ai_advisory_blockchain/
README.md
requirements.txt
```

## Installation

The repository uses one consolidated root `requirements.txt`.

Install dependencies using:

```bash
pip install -r requirements.txt
```

Core dependencies include:

- pandas
- numpy
- matplotlib
- plotly
- scikit-learn
- openpyxl

SQLite is accessed using Python's built-in `sqlite3` module.

## Part 1 — Payments & Fraud Analytics

Directory:

`payments_fraud_analytics/`

Run the fixed data generator from inside the directory:

```bash
cd payments_fraud_analytics
python generate_data.py
```

Then run:

```bash
python create_database.py
python run_fraud_queries.py
python reconcile.py
python dashboard.py
```

This module includes spreadsheet merchant analysis, normalized SQLite fraud analysis, payment reconciliation, and a four-layer code-generated dashboard.

See `payments_fraud_analytics/README.md` for detailed assumptions, results, and dashboard interpretation.

## Part 2 — Credit Risk & Lending ML

Directory:

`credit_risk_lending_ml/`

Generate the fixed data using:

```bash
cd credit_risk_lending_ml
python generate_data.py
```
Then run the complete modelling and anomaly-detection pipeline:

```bash
python credit_risk_modeling.py

The analysis covers thin-file handling, leakage-safe preprocessing, Logistic Regression, Decision Tree classification, risk-based pricing, Isolation Forest anomaly detection, and model-governance considerations.

See `credit_risk_lending_ml/README.md` for measured results and the final recommendation.

## Part 3 — AI Advisory & Blockchain Risk

Directory:

`ai_advisory_blockchain/`

The graded baseline uses deterministic mock mode. Leave `MOCK_LLM` unset or use:

```bash
MOCK_LLM=1
```

Run:

```bash
python advisory_agent.py
python extract_disclosure.py
python debate.py
python dcf_calculator.py
```

This module includes a think-act-observe portfolio advisory agent, CAPM and portfolio-risk calculations, human-advisor escalation, structured disclosure extraction, a multi-agent debate, DCF valuation, and a blockchain/crypto risk appendix.

See `ai_advisory_blockchain/README.md` for assumptions and recorded outputs.

## Design Decisions

### Payments

The exact seeded transaction generator is retained to make all fraud patterns and reconciliation discrepancies reproducible. Spreadsheet functionality represents regional analyst workflows, while SQL and Python handle relational fraud detection and reconciliation.

### Lending

Thin-file applicants are retained rather than discarded. Missing bureau scores are imputed only after the train/test split using a training-derived median, while scaling and encoding are fitted only on training data to avoid leakage.

### Advisory

The portfolio advisory workflow follows the prescribed risk-tolerance allocation table rather than optimizing weights. CAPM expected return uses beta only, portfolio calculations assume a constant pairwise correlation of 0.30, and portfolios with standard deviation above 20% are escalated to a human advisor.

All required AI-assisted functions operate successfully in deterministic mock mode without a paid API or network dependency.
