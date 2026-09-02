
import json
from disclosure_snippets import DISCLOSURE_SNIPPETS


def extract_signals(snippet: str) -> dict:

    text = snippet.lower()

    risk_flags = []

    if "litigation" in text:
        risk_flags.append("litigation")

    if (
        "regulatory" in text
        or "regulator" in text
    ):
        risk_flags.append(
            "regulatory"
        )

    if (
        "top three customers" in text
        or "customer concentration" in text
    ):
        risk_flags.append(
            "customer concentration"
        )

    hedging_terms = [
        "assuming",
        "cautiously",
        "visibility"
    ]

    hedging_detected = any(
        term in text
        for term in hedging_terms
    )

    if (
        "confident" in text
        or "approved" in text
    ):
        sentiment = "confident"

    elif hedging_detected:
        sentiment = "cautious"

    else:
        sentiment = "neutral"

    return {
        "risk_flags":
            risk_flags,

        "hedging_detected":
            hedging_detected,

        "sentiment":
            sentiment
    }


def main():

    outputs = []

    for snippet in DISCLOSURE_SNIPPETS:

        doc_id = snippet.split(":")[0]

        result = extract_signals(
            snippet
        )

        output = {
            "document_id":
                doc_id,

            "snippet":
                snippet,

            **result
        }

        outputs.append(output)

        print(
            doc_id,
            "->",
            result
        )

    with open(
        "disclosure_results.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            outputs,
            f,
            indent=2
        )


if __name__ == "__main__":
    main()
