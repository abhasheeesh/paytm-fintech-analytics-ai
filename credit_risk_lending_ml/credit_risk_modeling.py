import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import IsolationForest
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    ConfusionMatrixDisplay,
    RocCurveDisplay
)


# =========================================================
# 1. LOAD CREDIT DATA
# =========================================================

credit = pd.read_csv("credit_applicants.csv")

print("Applicants:", len(credit))
print("Default rate:", f"{credit['default'].mean():.2%}")
print(
    "Missing bureau score:",
    f"{credit['credit_bureau_score'].isna().mean():.2%}"
)


# =========================================================
# 2. THIN-FILE FLAG
# =========================================================

# Create this BEFORE imputation.
credit["is_thin_file"] = (
    credit["credit_bureau_score"]
    .isna()
    .astype(int)
)


# =========================================================
# 3. TRAIN / TEST SPLIT
# =========================================================

X = credit.drop(columns=["default"])
y = credit["default"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)


# =========================================================
# 4. TRAINING-ONLY BUREAU MEDIAN IMPUTATION
# =========================================================

training_bureau_median = (
    X_train["credit_bureau_score"]
    .dropna()
    .median()
)

print(
    "Training-only bureau median:",
    training_bureau_median
)

X_train = X_train.copy()
X_test = X_test.copy()

X_train["credit_bureau_score"] = (
    X_train["credit_bureau_score"]
    .fillna(training_bureau_median)
)

X_test["credit_bureau_score"] = (
    X_test["credit_bureau_score"]
    .fillna(training_bureau_median)
)


# =========================================================
# 5. FEATURES
# =========================================================

numeric_features = [
    "age",
    "monthly_income_inr",
    "existing_loans_count",
    "credit_utilization_ratio",
    "upi_monthly_inflow_inr",
    "bounced_payments_count",
    "credit_bureau_score",
    "is_thin_file"
]

categorical_features = [
    "employment_type"
]


# =========================================================
# 6. SCALE NUMERIC FEATURES
# =========================================================

scaler = StandardScaler()

X_train_numeric = scaler.fit_transform(
    X_train[numeric_features]
)

X_test_numeric = scaler.transform(
    X_test[numeric_features]
)


# =========================================================
# 7. ONE-HOT ENCODE EMPLOYMENT TYPE
# =========================================================

try:
    encoder = OneHotEncoder(
        handle_unknown="ignore",
        sparse_output=False
    )
except TypeError:
    # Compatibility with older scikit-learn versions
    encoder = OneHotEncoder(
        handle_unknown="ignore",
        sparse=False
    )

X_train_category = encoder.fit_transform(
    X_train[categorical_features]
)

X_test_category = encoder.transform(
    X_test[categorical_features]
)


X_train_final = np.hstack([
    X_train_numeric,
    X_train_category
])

X_test_final = np.hstack([
    X_test_numeric,
    X_test_category
])


# =========================================================
# 8. LOGISTIC REGRESSION
# =========================================================

logistic_model = LogisticRegression(
    max_iter=1000,
    random_state=42
)

logistic_model.fit(
    X_train_final,
    y_train
)

logistic_predictions = logistic_model.predict(
    X_test_final
)

logistic_probabilities = (
    logistic_model.predict_proba(
        X_test_final
    )[:, 1]
)


# =========================================================
# 9. DECISION TREE
# =========================================================

tree_model = DecisionTreeClassifier(
    random_state=42
)

tree_model.fit(
    X_train_final,
    y_train
)

tree_predictions = tree_model.predict(
    X_test_final
)

tree_probabilities = (
    tree_model.predict_proba(
        X_test_final
    )[:, 1]
)


# =========================================================
# 10. MODEL METRICS
# =========================================================

def model_metrics(
    name,
    actual,
    predictions,
    probabilities
):
    return {
        "model": name,
        "accuracy": accuracy_score(
            actual,
            predictions
        ),
        "precision": precision_score(
            actual,
            predictions,
            zero_division=0
        ),
        "recall": recall_score(
            actual,
            predictions
        ),
        "f1": f1_score(
            actual,
            predictions
        ),
        "roc_auc": roc_auc_score(
            actual,
            probabilities
        )
    }


results = pd.DataFrame([
    model_metrics(
        "Logistic Regression",
        y_test,
        logistic_predictions,
        logistic_probabilities
    ),
    model_metrics(
        "Decision Tree",
        y_test,
        tree_predictions,
        tree_probabilities
    )
])

print("\nModel comparison:")
print(results)

results.to_csv(
    "model_comparison.csv",
    index=False
)


# =========================================================
# 11. CONFUSION MATRICES
# =========================================================

fig, axes = plt.subplots(
    1,
    2,
    figsize=(10, 4)
)

ConfusionMatrixDisplay.from_predictions(
    y_test,
    logistic_predictions,
    ax=axes[0]
)

axes[0].set_title(
    "Logistic Regression"
)

ConfusionMatrixDisplay.from_predictions(
    y_test,
    tree_predictions,
    ax=axes[1]
)

axes[1].set_title(
    "Decision Tree"
)

plt.tight_layout()

plt.savefig(
    "confusion_matrices.png",
    dpi=180,
    bbox_inches="tight"
)

plt.close()


# =========================================================
# 12. ROC CURVES
# =========================================================

fig, ax = plt.subplots(
    figsize=(7, 5)
)

RocCurveDisplay.from_predictions(
    y_test,
    logistic_probabilities,
    name="Logistic Regression",
    ax=ax
)

RocCurveDisplay.from_predictions(
    y_test,
    tree_probabilities,
    name="Decision Tree",
    ax=ax
)

ax.plot(
    [0, 1],
    [0, 1],
    linestyle="--"
)

ax.set_title(
    "ROC Curves — Credit Default Models"
)

plt.tight_layout()

plt.savefig(
    "roc_curves.png",
    dpi=180,
    bbox_inches="tight"
)

plt.close()


# =========================================================
# 13. RISK-BASED PRICING
# =========================================================

pricing = pd.DataFrame({
    "applicant_id":
        X_test["applicant_id"].values,

    "predicted_default_probability":
        logistic_probabilities,

    "actual_default":
        y_test.values
})

pricing["risk_tier"] = pd.qcut(
    pricing[
        "predicted_default_probability"
    ],
    q=4,
    labels=[
        "Low",
        "Moderate",
        "High",
        "Very High"
    ]
)

rate_mapping = {
    "Low": "9%-11%",
    "Moderate": "12%-14%",
    "High": "15%-18%",
    "Very High": "19%-24%"
}

pricing[
    "illustrative_interest_rate"
] = pricing["risk_tier"].map(
    rate_mapping
)

pricing_summary = (
    pricing
    .groupby(
        "risk_tier",
        observed=False
    )
    .agg(
        applicants=(
            "applicant_id",
            "count"
        ),
        mean_predicted_pd=(
            "predicted_default_probability",
            "mean"
        ),
        observed_default_rate=(
            "actual_default",
            "mean"
        )
    )
    .reset_index()
)

pricing_summary[
    "illustrative_interest_rate"
] = pricing_summary[
    "risk_tier"
].map(rate_mapping)

pricing_summary.to_csv(
    "risk_pricing_table.csv",
    index=False
)

print("\nRisk-pricing table:")
print(pricing_summary)


# =========================================================
# 14. ISOLATION FOREST
# =========================================================

behaviour = pd.read_csv(
    "txn_behaviour.csv"
)

behaviour_features = [
    "txn_hour",
    "is_new_device",
    "txn_amount_inr"
]

behaviour_scaler = StandardScaler()

X_behaviour = (
    behaviour_scaler.fit_transform(
        behaviour[
            behaviour_features
        ]
    )
)

isolation_model = IsolationForest(
    random_state=42,
    contamination=15 / 265
)

behaviour[
    "isolation_prediction"
] = isolation_model.fit_predict(
    X_behaviour
)

behaviour[
    "flagged_anomaly"
] = (
    behaviour[
        "isolation_prediction"
    ] == -1
)

seeded_anomaly_mask = (
    behaviour["txn_id"]
    .str.startswith("BTXNA")
)

total_seeded = seeded_anomaly_mask.sum()

detected_seeded = behaviour.loc[
    seeded_anomaly_mask,
    "flagged_anomaly"
].sum()

isolation_recall = (
    detected_seeded
    / total_seeded
)

print(
    "\nSeeded anomalies:",
    total_seeded
)

print(
    "Seeded anomalies detected:",
    detected_seeded
)

print(
    "Isolation Forest recall:",
    f"{isolation_recall:.2%}"
)

behaviour.to_csv(
    "anomaly_detection_results.csv",
    index=False
)


# =========================================================
# 15. FINAL COMPARISON
# =========================================================

final_comparison = results.copy()

final_comparison[
    "isolation_forest_recall"
] = np.nan

isolation_row = pd.DataFrame([{
    "model": "Isolation Forest",
    "accuracy": np.nan,
    "precision": np.nan,
    "recall": np.nan,
    "f1": np.nan,
    "roc_auc": np.nan,
    "isolation_forest_recall":
        isolation_recall
}])

final_comparison = pd.concat(
    [
        final_comparison,
        isolation_row
    ],
    ignore_index=True
)

final_comparison.to_csv(
    "final_model_comparison.csv",
    index=False
)

print("\nFinal comparison:")
print(final_comparison)

print("\nCredit-risk pipeline completed successfully.")
