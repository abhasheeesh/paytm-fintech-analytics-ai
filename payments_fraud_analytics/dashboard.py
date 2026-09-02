
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "dashboard_outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# -----------------------------
# Load data
# -----------------------------

ledger = pd.read_csv(BASE_DIR / "ledger.csv")
gateway = pd.read_csv(BASE_DIR / "gateway_export.csv")
merchants = pd.read_csv(BASE_DIR / "merchants.csv")

ledger["transaction_time"] = pd.to_datetime(
    ledger["transaction_time"]
)

gateway["transaction_time"] = pd.to_datetime(
    gateway["transaction_time"]
)

# -----------------------------
# Headline metrics
# -----------------------------

# Design choice:
# GMV = total amount_inr across all ledger transactions.
total_gmv = ledger["amount_inr"].sum()

# Success = captured transaction / all ledger transactions
success_rate = (
    ledger["status"] == "captured"
).mean()

# Count-based platform chargeback ratio
chargeback_ratio = (
    ledger["status"] == "chargeback"
).mean()

# Exact reconciliation match definition
comparison = ledger.merge(
    gateway,
    on="transaction_id",
    how="inner",
    suffixes=("_ledger", "_gateway")
)

exact_match_count = (
    (
        comparison["amount_inr_ledger"]
        == comparison["amount_inr_gateway"]
    )
    &
    (
        comparison["status_ledger"]
        == comparison["status_gateway"]
    )
).sum()

match_rate = exact_match_count / len(ledger)

metrics = pd.DataFrame({
    "metric": [
        "total_gmv_inr",
        "success_rate",
        "match_rate",
        "chargeback_ratio"
    ],
    "value": [
        total_gmv,
        success_rate,
        match_rate,
        chargeback_ratio
    ]
})

metrics.to_csv(
    OUTPUT_DIR / "dashboard_metrics.csv",
    index=False
)

# -----------------------------
# Headline scorecards
# -----------------------------

fig, ax = plt.subplots(figsize=(10, 6))

ax.axis("off")

scorecards = [
    ("Total GMV", f"INR {total_gmv:,.0f}"),
    ("Success rate", f"{success_rate:.2%}"),
    (
        "Reconciliation match rate",
        f"{match_rate:.2%}"
    ),
    (
        "Chargeback ratio",
        f"{chargeback_ratio:.2%}"
    ),
]

y = 0.82

for label, value in scorecards:

    ax.text(
        0.05,
        y,
        label,
        fontsize=14,
        weight="bold",
        transform=ax.transAxes
    )

    ax.text(
        0.55,
        y,
        value,
        fontsize=16,
        transform=ax.transAxes
    )

    y -= 0.20

ax.set_title(
    "Payments Analytics — Headline Scorecards",
    fontsize=18,
    pad=20
)

fig.savefig(
    OUTPUT_DIR / "headline_scorecards.png",
    dpi=180,
    bbox_inches="tight"
)

plt.close(fig)

# -----------------------------
# Daily trends
# -----------------------------

ledger["transaction_date"] = (
    ledger["transaction_time"].dt.normalize()
)

daily = (
    ledger
    .groupby("transaction_date")
    .agg(
        daily_gmv_inr=(
            "amount_inr",
            "sum"
        ),
        daily_chargeback_count=(
            "status",
            lambda s: (
                s == "chargeback"
            ).sum()
        )
    )
    .reset_index()
)

full_dates = pd.DataFrame({
    "transaction_date": pd.date_range(
        ledger["transaction_date"].min(),
        ledger["transaction_date"].max(),
        freq="D"
    )
})

daily = full_dates.merge(
    daily,
    on="transaction_date",
    how="left"
)

daily = daily.fillna({
    "daily_gmv_inr": 0,
    "daily_chargeback_count": 0
})

fig, ax1 = plt.subplots(figsize=(11, 6))

line1 = ax1.plot(
    daily["transaction_date"],
    daily["daily_gmv_inr"],
    marker="o",
    label="Daily GMV (INR)"
)

ax1.set_xlabel("Date")
ax1.set_ylabel("Daily GMV (INR)")
ax1.tick_params(
    axis="x",
    rotation=45
)

ax2 = ax1.twinx()

line2 = ax2.plot(
    daily["transaction_date"],
    daily["daily_chargeback_count"],
    marker="s",
    linestyle="--",
    label="Daily chargebacks"
)

ax2.set_ylabel(
    "Chargeback count"
)

lines = line1 + line2

ax1.legend(
    lines,
    [line.get_label() for line in lines],
    loc="upper left"
)

ax1.set_title(
    "Daily GMV and Chargeback Count"
)

fig.tight_layout()

fig.savefig(
    OUTPUT_DIR / "daily_trends.png",
    dpi=180,
    bbox_inches="tight"
)

plt.close(fig)

# -----------------------------
# Merchant enrichment
# -----------------------------

merged = ledger.merge(
    merchants,
    on="merchant_id",
    how="left",
    validate="many_to_one"
)

# -----------------------------
# GMV by payment method
# -----------------------------

method_gmv = (
    merged
    .groupby(
        "payment_method",
        as_index=False
    )["amount_inr"]
    .sum()
    .sort_values(
        "amount_inr",
        ascending=False
    )
)

fig, ax = plt.subplots(
    figsize=(8, 5)
)

ax.bar(
    method_gmv["payment_method"],
    method_gmv["amount_inr"]
)

ax.set_title(
    "GMV by Payment Method"
)

ax.set_xlabel(
    "Payment method"
)

ax.set_ylabel(
    "GMV (INR)"
)

fig.tight_layout()

fig.savefig(
    OUTPUT_DIR /
    "gmv_by_payment_method.png",
    dpi=180,
    bbox_inches="tight"
)

plt.close(fig)

# -----------------------------
# GMV by category
# -----------------------------

category_gmv = (
    merged
    .groupby(
        "category",
        as_index=False
    )["amount_inr"]
    .sum()
    .sort_values(
        "amount_inr",
        ascending=False
    )
)

fig, ax = plt.subplots(
    figsize=(10, 5)
)

ax.bar(
    category_gmv["category"],
    category_gmv["amount_inr"]
)

ax.set_title(
    "GMV by Merchant Category"
)

ax.set_xlabel(
    "Category"
)

ax.set_ylabel(
    "GMV (INR)"
)

ax.tick_params(
    axis="x",
    rotation=30
)

fig.tight_layout()

fig.savefig(
    OUTPUT_DIR /
    "gmv_by_category.png",
    dpi=180,
    bbox_inches="tight"
)

plt.close(fig)

# -----------------------------
# Details layer
# -----------------------------

merchant_summary = (
    merged
    .groupby(
        [
            "merchant_id",
            "merchant_name"
        ],
        as_index=False
    )
    .agg(
        transaction_count=(
            "transaction_id",
            "count"
        ),
        chargeback_count=(
            "status",
            lambda s: (
                s == "chargeback"
            ).sum()
        )
    )
)

merchant_summary[
    "chargeback_ratio"
] = (
    merchant_summary[
        "chargeback_count"
    ]
    /
    merchant_summary[
        "transaction_count"
    ]
)

merchant_summary[
    "flag"
] = merchant_summary[
    "chargeback_ratio"
].apply(
    lambda x:
    "FLAG >1%"
    if x > 0.01
    else "OK"
)

top10 = (
    merchant_summary
    .sort_values(
        [
            "transaction_count",
            "merchant_id"
        ],
        ascending=[
            False,
            True
        ]
    )
    .head(10)
    .copy()
)

top10.to_csv(
    OUTPUT_DIR /
    "top10_merchants.csv",
    index=False
)

display_table = top10[
    [
        "merchant_id",
        "merchant_name",
        "transaction_count",
        "chargeback_count",
        "chargeback_ratio",
        "flag"
    ]
].copy()

display_table[
    "chargeback_ratio"
] = display_table[
    "chargeback_ratio"
].map(
    lambda x: f"{x:.2%}"
)

fig, ax = plt.subplots(
    figsize=(12, 5)
)

ax.axis("off")

table = ax.table(
    cellText=display_table.values,
    colLabels=display_table.columns,
    cellLoc="center",
    loc="center"
)

table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 1.5)

ax.set_title(
    "Top 10 Merchants by Transaction Count",
    pad=20
)

fig.tight_layout()

fig.savefig(
    OUTPUT_DIR /
    "top10_merchants.png",
    dpi=180,
    bbox_inches="tight"
)

plt.close(fig)

# -----------------------------
# Console summary
# -----------------------------

print(
    "Total GMV (INR):",
    f"{total_gmv:,.0f}"
)

print(
    "Success rate:",
    f"{success_rate:.2%}"
)

print(
    "Exact matched transactions:",
    exact_match_count
)

print(
    "Match rate:",
    f"{match_rate:.2%}"
)

print(
    "Chargeback ratio:",
    f"{chargeback_ratio:.2%}"
)

print(
    "Dashboard files saved to:",
    OUTPUT_DIR
)
