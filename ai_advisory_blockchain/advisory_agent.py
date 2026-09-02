
import os
import json
import math
from itertools import combinations

from stock_universe import (
    STOCK_UNIVERSE,
    RISK_FREE_RATE,
    MARKET_RETURN
)

from investor_profiles import INVESTOR_PROFILES


ALLOCATION_RULES = {
    "Conservative": [
        "PAYBOND",
        "PAYGOLD",
        "PAYRETAIL"
    ],
    "Moderate": [
        "PAYRETAIL",
        "PAYINFRA",
        "PAYGOLD"
    ],
    "Aggressive": [
        "PAYTECH",
        "PAYFIN",
        "PAYINFRA"
    ]
}

PAIRWISE_CORRELATION = 0.30


def get_stock_data(ticker):
    """
    Simulated external-data tool call.
    """
    return STOCK_UNIVERSE[ticker]


def think(investor):
    """
    THINK:
    Determine allocation from the prescribed risk-tolerance lookup.
    """
    risk_tolerance = investor["risk_tolerance"]

    tickers = ALLOCATION_RULES[risk_tolerance]

    weights = {
        ticker: 1 / 3
        for ticker in tickers
    }

    return tickers, weights


def act(tickers):
    """
    ACT:
    Retrieve stock data through get_stock_data().
    """
    return {
        ticker: get_stock_data(ticker)
        for ticker in tickers
    }


def capm_expected_return(beta):
    return (
        RISK_FREE_RATE
        + beta
        * (
            MARKET_RETURN
            - RISK_FREE_RATE
        )
    )


def observe_and_decide(
    investor,
    tickers,
    weights,
    stock_data
):
    """
    OBSERVE -> DECIDE:
    Compute CAPM return and portfolio volatility.
    """

    stock_capm_returns = {}

    for ticker in tickers:
        beta = stock_data[ticker]["beta"]

        stock_capm_returns[ticker] = (
            capm_expected_return(beta)
        )

    portfolio_return = sum(
        weights[ticker]
        * stock_capm_returns[ticker]
        for ticker in tickers
    )

    # Variance terms
    portfolio_variance = sum(
        (
            weights[ticker] ** 2
        )
        * (
            stock_data[ticker]["std_dev"] ** 2
        )
        for ticker in tickers
    )

    # Covariance terms
    for ticker_i, ticker_j in combinations(
        tickers,
        2
    ):

        covariance = (
            PAIRWISE_CORRELATION
            * stock_data[ticker_i]["std_dev"]
            * stock_data[ticker_j]["std_dev"]
        )

        portfolio_variance += (
            2
            * weights[ticker_i]
            * weights[ticker_j]
            * covariance
        )

    portfolio_std = math.sqrt(
        portfolio_variance
    )

    if portfolio_std > 0.20:
        status = "ESCALATED_TO_HUMAN_ADVISOR"
    else:
        status = "FINALIZED"

    return {
        "investor_id":
            investor["investor_id"],

        "risk_tolerance":
            investor["risk_tolerance"],

        "tickers":
            tickers,

        "weights":
            weights,

        "portfolio_expected_return":
            portfolio_return,

        "portfolio_variance":
            portfolio_variance,

        "portfolio_std":
            portfolio_std,

        "status":
            status
    }


def create_narrative(result):
    """
    Graded baseline:
    deterministic mock mode.
    """

    mock_llm = os.getenv(
        "MOCK_LLM",
        "1"
    )

    if mock_llm != "0":

        tickers = ", ".join(
            result["tickers"]
        )

        return (
            f"For {result['risk_tolerance']} investor "
            f"{result['investor_id']}, we recommend "
            f"an equal allocation across {tickers}, "
            f"with an expected CAPM portfolio return "
            f"of {result['portfolio_expected_return']:.1%} "
            f"and volatility of "
            f"{result['portfolio_std']:.1%}. "
            f"Decision status: {result['status']}."
        )

    # Optional live-LLM extension deliberately
    # not required for graded baseline.
    return create_narrative({
        **result
    })


def run_agent(investor):

    # THINK
    tickers, weights = think(investor)

    # ACT
    stock_data = act(tickers)

    # OBSERVE -> DECIDE
    result = observe_and_decide(
        investor,
        tickers,
        weights,
        stock_data
    )

    result["narrative"] = (
        create_narrative(result)
    )

    return result


def main():

    results = []

    for investor in INVESTOR_PROFILES:

        result = run_agent(investor)

        results.append(result)

        print(
            result["investor_id"],
            "|",
            result["risk_tolerance"],
            "| return:",
            f"{result['portfolio_expected_return']:.2%}",
            "| volatility:",
            f"{result['portfolio_std']:.2%}",
            "|",
            result["status"]
        )

    with open(
        "advisory_results.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            results,
            f,
            indent=2
        )


if __name__ == "__main__":
    main()
