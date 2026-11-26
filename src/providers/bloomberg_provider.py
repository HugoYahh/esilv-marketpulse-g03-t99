import json
from pathlib import Path

BLOOMBERG_IDENTIFIERS = {
    "AAPL": "AAPL US Equity",
    "SP500": "SPX Index",
}

BLOOMBERG_ACCESS_MODE = "APPROVED_SAMPLE"

SAMPLE_FILE = (
    Path(__file__).resolve().parent.parent.parent
    / "data"
    / "sample"
    / "bloomberg_reference_sample.json"
)


def fetch_raw_bloomberg_history(identifier, start_date=None, end_date=None):
    if BLOOMBERG_ACCESS_MODE != "APPROVED_SAMPLE":
        raise NotImplementedError("LIVE Bloomberg connection is not configured.")

    with open(SAMPLE_FILE, encoding="utf-8") as f:
        payload = json.load(f)

    for series in payload.get("series", []):
        if series.get("provider_identifier") == identifier:
            return series

    raise ValueError(f"Identifier {identifier} not found in approved sample.")


def normalize_bloomberg_history(raw_data, canonical_ticker):
    rows = []
    for obs in raw_data.get("observations", []):
        rows.append(
            {
                "date": obs["observation_date"],
                "ticker": canonical_ticker,
                "open": float(obs["open_value"]),
                "high": float(obs["high_value"]),
                "low": float(obs["low_value"]),
                "close": float(obs["close_value"]),
                "volume": int(obs["volume_value"]),
            }
        )
    return sorted(rows, key=lambda row: row["date"])


def fetch_bloomberg_prices(canonical_ticker, start_date=None, end_date=None):
    if canonical_ticker not in BLOOMBERG_IDENTIFIERS:
        raise ValueError(f"Ticker {canonical_ticker} not supported by Bloomberg provider")

    identifier = BLOOMBERG_IDENTIFIERS[canonical_ticker]
    raw_data = fetch_raw_bloomberg_history(identifier, start_date, end_date)
    return normalize_bloomberg_history(raw_data, canonical_ticker)