
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "dashboard_outputs"

required_files = [
    "headline_scorecards.png",
    "daily_trends.png",
    "gmv_by_payment_method.png",
    "gmv_by_category.png",
    "top10_merchants.png",
    "dashboard_metrics.csv",
    "top10_merchants.csv"
]

for file in required_files:

    path = OUTPUT_DIR / file

    assert path.exists(), (
        f"Missing file: {file}"
    )

    assert path.stat().st_size > 0, (
        f"Empty file: {file}"
    )

metrics = pd.read_csv(
    OUTPUT_DIR /
    "dashboard_metrics.csv"
)

metric_dict = dict(
    zip(
        metrics["metric"],
        metrics["value"]
    )
)

assert (
    metric_dict[
        "total_gmv_inr"
    ]
    == 382603
)

assert abs(
    metric_dict[
        "success_rate"
    ]
    - 468 / 547
) < 1e-10

assert abs(
    metric_dict[
        "match_rate"
    ]
    - 495 / 547
) < 1e-10

assert abs(
    metric_dict[
        "chargeback_ratio"
    ]
    - 28 / 547
) < 1e-10

top10 = pd.read_csv(
    OUTPUT_DIR /
    "top10_merchants.csv"
)

assert len(top10) == 10

assert (
    top10[
        "chargeback_ratio"
    ]
    >= 0
).all()

workbook = (
    BASE_DIR /
    "merchant_workbook.xlsx"
)

assert workbook.exists()
assert workbook.stat().st_size > 0

print(
    "PASS — merchant_workbook.xlsx exists"
)

print(
    "PASS — all required dashboard files exist"
)

print(
    "PASS — Total GMV = INR 382,603"
)

print(
    "PASS — Success rate = 85.56%"
)

print(
    "PASS — Match rate = 90.49%"
)

print(
    "PASS — Chargeback ratio = 5.12%"
)

print(
    "PASS — top-10 merchant output contains 10 rows"
)

print()
print(
    "PART 1 DASHBOARD CORE CHECKS PASSED"
)
