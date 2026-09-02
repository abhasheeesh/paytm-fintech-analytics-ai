
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent


def reconcile_payments(ledger_df, gateway_df):
    """
    Compare Paytm ledger transactions against gateway transactions.

    Returns:
        missing_in_gateway
        missing_in_ledger
        amount_mismatches
        status_mismatches
    """

    ledger_ids = set(ledger_df["transaction_id"])
    gateway_ids = set(gateway_df["transaction_id"])

    # Present in ledger but absent from gateway
    missing_gateway_ids = ledger_ids - gateway_ids

    missing_in_gateway = ledger_df[
        ledger_df["transaction_id"].isin(missing_gateway_ids)
    ].copy()

    # Present in gateway but absent from ledger
    missing_ledger_ids = gateway_ids - ledger_ids

    missing_in_ledger = gateway_df[
        gateway_df["transaction_id"].isin(missing_ledger_ids)
    ].copy()

    # Compare transactions present in both datasets
    common = pd.merge(
        ledger_df,
        gateway_df,
        on="transaction_id",
        how="inner",
        suffixes=("_ledger", "_gateway")
    )

    # Amount mismatches
    amount_mismatches = common[
        common["amount_inr_ledger"] != common["amount_inr_gateway"]
    ].copy()

    amount_mismatches["amount_difference_inr"] = (
        amount_mismatches["amount_inr_gateway"]
        - amount_mismatches["amount_inr_ledger"]
    )

    # Status mismatches
    status_mismatches = common[
        common["status_ledger"] != common["status_gateway"]
    ].copy()

    return (
        missing_in_gateway,
        missing_in_ledger,
        amount_mismatches,
        status_mismatches
    )


def main():

    ledger = pd.read_csv(BASE_DIR / "ledger.csv")
    gateway = pd.read_csv(BASE_DIR / "gateway_export.csv")

    (
        missing_in_gateway,
        missing_in_ledger,
        amount_mismatches,
        status_mismatches
    ) = reconcile_payments(ledger, gateway)

    output_dir = BASE_DIR / "reconciliation_outputs"
    output_dir.mkdir(exist_ok=True)

    missing_in_gateway.to_csv(
        output_dir / "missing_in_gateway.csv",
        index=False
    )

    missing_in_ledger.to_csv(
        output_dir / "extra_in_gateway.csv",
        index=False
    )

    amount_mismatches.to_csv(
        output_dir / "amount_mismatches.csv",
        index=False
    )

    status_mismatches.to_csv(
        output_dir / "status_mismatches.csv",
        index=False
    )

    print("Missing in gateway:", len(missing_in_gateway))
    print("Extra in gateway:", len(missing_in_ledger))
    print("Amount mismatches:", len(amount_mismatches))
    print("Status mismatches:", len(status_mismatches))


if __name__ == "__main__":
    main()
