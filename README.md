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

---

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

This module includes spreadsheet-based merchant analysis, normalized SQLite fraud analysis, payment reconciliation, and a four-layer code-generated dashboard.

The spreadsheet artifact `merchant_workbook.xlsx` demonstrates VLOOKUP with fixed absolute references, IFERROR handling, HLOOKUP, nested IF/AND logic, pivot-table analysis, and transaction-count versus unique-days comparison.

See `payments_fraud_analytics/README.md` for detailed assumptions, fraud-detection results, reconciliation findings, and dashboard interpretation.

---

## Part 2 — Credit Risk & Lending ML

Directory:

`credit_risk_lending_ml/`

Generate the fixed synthetic datasets from inside the directory:

```bash
cd credit_risk_lending_ml
python generate_data.py
```

Then run the complete modelling and anomaly-detection pipeline:

```bash
python credit_risk_modeling.py
```

The analysis covers:

- thin-file applicant handling;
- a stratified 75/25 train/test split;
- training-only bureau-score median imputation;
- training-only feature scaling and categorical encoding;
- Logistic Regression;
- Decision Tree classification;
- confusion matrices, ROC curves, and ROC-AUC;
- risk-based pricing;
- Isolation Forest anomaly detection;
- bias and model-governance considerations.

The fixed applicant dataset contains 400 applicants, including 80 thin-file applicants with missing bureau scores. The measured default rate is 20.25%.

See `credit_risk_lending_ml/README.md` for measured model performance, risk-pricing results, anomaly-detection recall, bias-awareness discussion, and the final deployment recommendation.

---

## Part 3 — AI Advisory & Blockchain Risk

Directory:

`ai_advisory_blockchain/`

The graded baseline uses deterministic mock mode. No paid API or external LLM service is required.

Leave `MOCK_LLM` unset or use:

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

This module includes:

- a think-act-observe portfolio advisory agent;
- CAPM expected-return calculations;
- portfolio-variance and volatility calculations;
- human-advisor escalation for portfolios exceeding the prescribed volatility threshold;
- structured disclosure extraction;
- a bull/bear/synthesizer debate;
- DCF valuation and sensitivity analysis;
- a blockchain and crypto risk appendix.

The portfolio advisory workflow follows the prescribed equal-weight allocation rules for Conservative, Moderate, and Aggressive investors. CAPM expected returns use beta only, while portfolio variance assumes a constant pairwise correlation of 0.30.

See `ai_advisory_blockchain/README.md` for detailed assumptions, recorded mock-mode outputs, DCF results, and valuation sensitivity analysis.

---

## Design Decisions

### Payments

The exact seeded transaction generator is retained so that fraud patterns and reconciliation discrepancies are fully reproducible. Spreadsheet functionality represents analyst-style merchant operations, while SQL is used for relational fraud-pattern detection and Python is used for payment reconciliation and dashboard generation.

The reconciliation match rate uses the stricter project definition: a transaction is counted as matched only when it exists in both the ledger and gateway export with identical `amount_inr` and `status`.

### Lending

Thin-file applicants are retained rather than discarded because alternative payment and UPI behaviour can provide useful signals where formal bureau history is unavailable.

The `is_thin_file` indicator is created before imputation. Missing bureau scores are imputed only after the train/test split using a median calculated from non-missing training observations. Feature scaling and categorical encoding are also fitted only on training data to avoid test-set leakage.

Both Logistic Regression and Decision Tree models are evaluated on the same stratified split. Logistic Regression predicted default probabilities are additionally used to create illustrative risk-based pricing tiers.

### Advisory

The portfolio advisory workflow follows the prescribed risk-tolerance allocation table rather than optimizing portfolio weights. CAPM expected return uses beta only and does not use the separate `analyst_expected_return` field.

Portfolio calculations assume a constant pairwise correlation of 0.30. Portfolios with computed standard deviation above 20% are escalated to a human advisor.

All required AI-assisted functions operate successfully in deterministic `MOCK_LLM` mode without a paid API, API key, or network dependency.

---

## Key Outputs

### Payments & Fraud Analytics

- `merchant_workbook.xlsx`
- `paytm_payments.db`
- `fraud_queries.sql`
- `sql_outputs/`
- `reconciliation_outputs/`
- `dashboard_outputs/`

### Credit Risk & Lending ML

- `model_comparison.csv`
- `risk_pricing_table.csv`
- `anomaly_detection_results.csv`
- `final_model_comparison.csv`
- `confusion_matrices.png`
- `roc_curves.png`

### AI Advisory & Blockchain Risk

- `advisory_results.json`
- `disclosure_results.json`
- `debate_output.txt`
- `dcf_projection.csv`
- `dcf_sensitivity.csv`
- `blockchain_risk_note.md`

---

## Reproducibility

The project uses the fixed random seeds prescribed in the capstone brief. Part 1 and Part 2 data generators should be run from their respective directories so that generated CSV files are written to the correct locations.

The required Part 3 workflow is fully deterministic when `MOCK_LLM` is unset or set to `1`.
