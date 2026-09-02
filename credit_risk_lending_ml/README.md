
# Part 2 — Credit Risk & Lending ML

## Overview

This module builds a Paytm Postpaid-style credit-risk and behavioural anomaly-detection pipeline using the supplied synthetic datasets and scikit-learn.

## Dataset

The fixed generator produces:

- 400 credit applicants
- 81 defaults
- measured default rate of 20.25%
- exactly 80 thin-file applicants
- 265 transaction-behaviour rows
- 15 deliberately injected behavioural anomalies

## Thin-File and Preprocessing Strategy

The `is_thin_file` indicator is created directly from the raw missingness before any imputation. Thin-file applicants are retained rather than dropped because these applicants are precisely the population for whom alternative payment and UPI signals may be useful.

The dataset is split 75/25 using `random_state=42` and stratification on `default`. Stratification helps preserve the minority default class at a similar proportion in both train and test samples.

Missing bureau scores are imputed only after the split. The median is calculated from non-missing bureau scores in the training data only and that same training-derived value is then applied to both train and test sets. Numeric scaling and categorical encoding are also fitted only on training data to avoid leakage.

`employment_type` is one-hot encoded because the categories do not have a natural ordinal ranking.

## Model Comparison

Two classifiers are trained on the identical split:

- Logistic Regression
- Decision Tree Classifier

Logistic Regression achieved approximately:

- Accuracy: 76.0%
- Precision: 38.9%
- Recall: 35.0%
- F1: 36.8%
- ROC-AUC: 71.9%

Decision Tree achieved approximately:

- Accuracy: 67.0%
- Precision: 24.0%
- Recall: 30.0%
- F1: 26.7%
- ROC-AUC: 53.1%

Confusion matrices and ROC curves are saved as:

- `confusion_matrices.png`
- `roc_curves.png`

## Risk-Based Pricing

Logistic Regression predicted default probabilities are divided into four risk tiers:

- Low
- Moderate
- High
- Very High

Illustrative interest-rate ranges rise with predicted risk. The observed default rate for each tier is reported in `risk_pricing_table.csv` to check whether realized defaults increase materially with predicted risk.

## Anomaly Detection

Isolation Forest uses:

- `txn_hour`
- `is_new_device`
- `txn_amount_inr`

with standardized inputs and contamination equal to `15/265`.

The model identified 11 of the 15 seeded anomalies, giving recall of 73.33%.

## Bias-Awareness Note

Even though this dataset does not contain explicit variables such as gender, caste, religion, or location, that does not necessarily mean the model is free from bias. Some of the variables used here could still act as indirect proxies for protected or socio-economic characteristics in a real lending environment.

For example, `monthly_income_inr` is clearly relevant for assessing repayment capacity, but income is also closely connected with broader socio-economic conditions and unequal access to opportunities. Similarly, `employment_type` may appear to be a neutral variable, but categories such as salaried, self-employed, and gig work can indirectly capture structural differences in job stability, access to formal employment, and financial security. A model could therefore end up treating certain groups less favourably even without directly observing their protected characteristics.

`credit_bureau_score` creates a slightly different concern. Applicants with a long history of formal borrowing generally have more information available to the bureau, while younger applicants or people who have relied less on formal credit may have little or no bureau history. In this dataset, 80 applicants are thin-file customers with no bureau score. Simply dropping them would effectively exclude the exact group for whom alternative signals such as UPI inflows and payment behaviour may be most useful.

For this reason, I would not allow the model to make completely automatic final decisions for every applicant. A maker-checker or human-review process should be used particularly for declined thin-file applicants. In addition, the model should be subject to periodic fairness audits, subgroup performance monitoring, and logging of manual overrides. The objective should not just be to maximize predictive accuracy, but to ensure that the model's errors are understood and that applicants are not systematically disadvantaged because of variables acting as hidden proxies.

## Final Model Comparison

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC | Anomaly Recall |
|---|---:|---:|---:|---:|---:|---:|
| Logistic Regression | 76.0% | 38.9% | 35.0% | 36.8% | 71.9% | — |
| Decision Tree | 67.0% | 24.0% | 30.0% | 26.7% | 53.1% | — |
| Isolation Forest | — | — | — | — | — | 73.33% |

Isolation Forest is evaluated separately because it performs unsupervised behavioural anomaly detection rather than applicant default classification. Its recall represents detection of 11 of the 15 deliberately injected anomalies.

## Final Model Recommendation

I would choose Logistic Regression as the primary credit-risk classifier for this use case. It performed better than the Decision Tree across almost every important metric, with 76.0% accuracy compared with 67.0%, a higher F1 score of 36.8% versus 26.7%, and a substantially stronger ROC-AUC of 71.9% compared with 53.1%. Its recall is still only 35.0%, so I would not treat the model as sufficient for fully automated lending decisions, especially when missing an actual defaulter can be costly. The Isolation Forest also adds value on the fraud side by identifying 11 of the 15 deliberately injected anomalies, giving recall of 73.33%, so I would use it as a separate behavioural-risk flag rather than as a replacement for the credit classifier.
