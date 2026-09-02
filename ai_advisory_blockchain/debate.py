
from stock_universe import STOCK_UNIVERSE


TICKER = "PAYTECH"


def bull_agent(ticker, data):

    return (
        f"Bull view: {ticker} has an illustrative "
        f"analyst expected return of "
        f"{data['analyst_expected_return']:.1%}. "
        f"With beta {data['beta']:.2f}, it offers "
        f"meaningful upside for an investor willing "
        f"to accept above-market systematic risk."
    )


def bear_agent(ticker, data):

    return (
        f"Bear view: {ticker} carries a standard "
        f"deviation of {data['std_dev']:.1%} and "
        f"a beta of {data['beta']:.2f}. "
        f"That level of volatility means potential "
        f"returns come with substantial downside risk."
    )


def synthesizer(
    ticker,
    bull,
    bear
):

    return (
        f"Synthesis: The case for {ticker} combines "
        f"higher return potential with materially "
        f"higher volatility and systematic risk. "
        f"The asset may fit an aggressive portfolio, "
        f"but the risk highlighted by the bear case "
        f"should prevent the expected-return figure "
        f"from being considered in isolation."
    )


def main():

    data = STOCK_UNIVERSE[TICKER]

    bull = bull_agent(
        TICKER,
        data
    )

    bear = bear_agent(
        TICKER,
        data
    )

    synthesis = synthesizer(
        TICKER,
        bull,
        bear
    )

    output = (
        bull
        + "\n\n"
        + bear
        + "\n\n"
        + synthesis
    )

    print(output)

    with open(
        "debate_output.txt",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(output)


if __name__ == "__main__":
    main()
