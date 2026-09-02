
import pandas as pd

from stock_universe import (
    STOCK_UNIVERSE,
    RISK_FREE_RATE,
    MARKET_RETURN
)


# -------------------------
# Base FCFF assumptions
# -------------------------

EBIT = 120_000_000
TAX_RATE = 0.25
DA = 20_000_000
CAPEX = 30_000_000
DELTA_NWC = 10_000_000

BASE_FCFF = (
    EBIT * (1 - TAX_RATE)
    + DA
    - CAPEX
    - DELTA_NWC
)

# -------------------------
# Growth assumptions
# -------------------------

GROWTH_RATES = [
    0.18,
    0.16,
    0.14,
    0.12,
    0.10
]

TERMINAL_GROWTH = 0.075

# -------------------------
# WACC
# -------------------------

BETA = STOCK_UNIVERSE[
    "PAYINFRA"
]["beta"]

COST_OF_EQUITY = (
    RISK_FREE_RATE
    + BETA
    * (
        MARKET_RETURN
        - RISK_FREE_RATE
    )
)

PRETAX_COST_OF_DEBT = 0.09

AFTER_TAX_COST_OF_DEBT = (
    PRETAX_COST_OF_DEBT
    * (1 - TAX_RATE)
)

EQUITY_WEIGHT = 0.80
DEBT_WEIGHT = 0.20

WACC = (
    EQUITY_WEIGHT
    * COST_OF_EQUITY
    +
    DEBT_WEIGHT
    * AFTER_TAX_COST_OF_DEBT
)


def enterprise_value(
    wacc,
    terminal_growth
):

    fcff = BASE_FCFF

    projected = []

    pv_fcff = 0

    for year, growth in enumerate(
        GROWTH_RATES,
        start=1
    ):

        fcff *= (1 + growth)

        projected.append(fcff)

        pv_fcff += (
            fcff
            / (
                (1 + wacc)
                ** year
            )
        )

    fcff_6 = (
        projected[-1]
        * (1 + terminal_growth)
    )

    terminal_value = (
        fcff_6
        / (
            wacc
            - terminal_growth
        )
    )

    pv_terminal = (
        terminal_value
        / (
            (1 + wacc)
            ** 5
        )
    )

    return (
        pv_fcff
        + pv_terminal
    )


print(
    "Base FCFF:",
    f"INR {BASE_FCFF:,.0f}"
)

print(
    "Cost of equity:",
    f"{COST_OF_EQUITY:.2%}"
)

print(
    "After-tax cost of debt:",
    f"{AFTER_TAX_COST_OF_DEBT:.2%}"
)

print(
    "WACC:",
    f"{WACC:.2%}"
)

print(
    "Terminal growth:",
    f"{TERMINAL_GROWTH:.2%}"
)

base_ev = enterprise_value(
    WACC,
    TERMINAL_GROWTH
)

print(
    "DCF Enterprise Value:",
    f"INR {base_ev:,.0f}"
)


# -------------------------
# 3 x 3 sensitivity
# -------------------------

wacc_values = [
    WACC - 0.01,
    WACC,
    WACC + 0.01
]

growth_values = [
    TERMINAL_GROWTH - 0.01,
    TERMINAL_GROWTH,
    TERMINAL_GROWTH + 0.01
]

sensitivity = pd.DataFrame(
    index=[
        f"{x:.2%}"
        for x in wacc_values
    ],
    columns=[
        f"{x:.2%}"
        for x in growth_values
    ]
)

for w in wacc_values:

    for g in growth_values:

        assert w > g

        sensitivity.loc[
            f"{w:.2%}",
            f"{g:.2%}"
        ] = enterprise_value(
            w,
            g
        )

sensitivity.index.name = "WACC"

sensitivity.to_csv(
    "dcf_sensitivity.csv"
)

print("\nDCF sensitivity:")
print(sensitivity)


# Required worst-case check
worst_case_gap = (
    min(wacc_values)
    - max(growth_values)
)

print(
    "\nWorst-case WACC minus g:",
    f"{worst_case_gap:.2%}"
)

assert worst_case_gap >= 0.01


# -------------------------
# EV / EBITDA cross-check
# -------------------------

ILLUSTRATIVE_EBITDA = 160_000_000
EV_EBITDA_MULTIPLE = 8.0

multiple_ev = (
    ILLUSTRATIVE_EBITDA
    * EV_EBITDA_MULTIPLE
)

print(
    "EV/EBITDA implied EV:",
    f"INR {multiple_ev:,.0f}"
)
