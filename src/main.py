import csv
import json
from pathlib import Path

from analytics import (
    align_series,
    calculated_period_return,
    calculate_base_100,
    calculate_relative_performance,
)
from providers.bloomberg_provider import (
    BLOOMBERG_ACCESS_MODE,
    fetch_bloomberg_prices,
)
from providers.yahoo_provider import fetch_yahoo_prices

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "sample"

PERIOD = "1 month"
INTERVAL = "Daily"
PROVIDER = "bloomberg"

# parameters for Yahoo Finance API
YAHOO_LOOKBACK = "1mo"
YAHOO_INTERVAL = "1d"


def load_instruments():
    """Lit instruments.json et renvoie un dictionnaire."""
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as f:
        return json.load(f)


def load_prices():
    """Lit prices.csv et renvoie une liste de lignes (dictionnaires)."""
    with open(DATA_DIR / "prices.csv", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def filter_prices(prices, ticker):
    """Garde uniquement les lignes du ticker demandé."""
    result = []
    for row in prices:
        if row["ticker"] == ticker:
            result.append(row)
    return result


def get_prices(ticker, provider=PROVIDER, lookback=YAHOO_LOOKBACK, interval=YAHOO_INTERVAL):
    """Renvoie les lignes canoniques d'un ticker, selon le provider choisi."""
    if provider == "bloomberg":
        return fetch_bloomberg_prices(ticker)
    if provider == "yahoo":
        return fetch_yahoo_prices(ticker, lookback, interval)
    if provider == "csv":
        return filter_prices(load_prices(), ticker)
    raise ValueError(f"Provider inconnu : {provider}")


def get_first_date(prices):
    return prices[0]["date"]


def get_last_date(prices):
    return prices[-1]["date"]


def get_first_close(prices):
    """Renvoie le premier cours de clôture, converti en nombre."""
    return float(prices[0]["close"])


def get_last_close(prices):
    """Renvoie le dernier cours de clôture, converti en nombre."""
    return float(prices[-1]["close"])


def build_market_snapshot(provider=PROVIDER, lookback=YAHOO_LOOKBACK, interval=YAHOO_INTERVAL):
    """Construit le snapshot applicatif partagé (terminal + futur dashboard TD11)."""
    instruments = load_instruments()
    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    instrument_prices = get_prices(instrument["ticker"], provider=provider, lookback=lookback, interval=interval)
    benchmark_prices = get_prices(benchmark["ticker"], provider=provider, lookback=lookback, interval=interval)

    aligned_instrument, aligned_benchmark = align_series(instrument_prices, benchmark_prices)

    instrument_return = calculated_period_return(aligned_instrument)
    benchmark_return = calculated_period_return(aligned_benchmark)
    relative_performance = calculate_relative_performance(instrument_return, benchmark_return)

    instrument_base_100 = calculate_base_100(aligned_instrument)
    benchmark_base_100 = calculate_base_100(aligned_benchmark)

    access_mode = BLOOMBERG_ACCESS_MODE if provider == "bloomberg" else "STANDARD"

    return {
        "provider": provider,
        "access_mode": access_mode,
        "lookback": lookback,
        "interval": interval,
        "period": PERIOD,
        "display_interval": INTERVAL,
        "instrument": instrument,
        "benchmark": benchmark,
        "instrument_prices": instrument_prices,
        "benchmark_prices": benchmark_prices,
        "aligned_instrument": aligned_instrument,
        "aligned_benchmark": aligned_benchmark,
        "instrument_return": instrument_return,
        "benchmark_return": benchmark_return,
        "relative_performance": relative_performance,
        "instrument_base_100": instrument_base_100,
        "benchmark_base_100": benchmark_base_100,
    }


def display_market_summary(asset, prices, show_currency=True):
    """Affiche le résumé d'une série (instrument ou benchmark)."""
    first_close = get_first_close(prices)
    last_close = get_last_close(prices)
    first_date = get_first_date(prices)
    last_date = get_last_date(prices)

    currency = f" {asset['currency']}" if show_currency else ""

    print(f"{asset['ticker']} - {asset['name']}")
    print(f"Market       : {asset['market']}")
    print(f"Observations : {len(prices)}")
    print(f"First date   : {first_date}")
    print(f"Last date    : {last_date}")
    print(f"First close  : {first_close:.2f}{currency}")
    print(f"Last close   : {last_close:.2f}{currency}")


def main():
    snapshot = build_market_snapshot()

    instrument = snapshot["instrument"]
    benchmark = snapshot["benchmark"]
    aligned_instrument = snapshot["aligned_instrument"]
    aligned_benchmark = snapshot["aligned_benchmark"]
    instrument_return = snapshot["instrument_return"]
    benchmark_return = snapshot["benchmark_return"]
    relative_performance = snapshot["relative_performance"]
    instrument_base_100 = snapshot["instrument_base_100"]
    benchmark_base_100 = snapshot["benchmark_base_100"]

    provider_label = "Bloomberg stage" if snapshot["provider"] == "bloomberg" else snapshot["provider"]

    print("=== MarketPulse ===")
    print()
    print("Market configuration")
    print(f"Provider    : {provider_label}")
    if snapshot["provider"] == "bloomberg":
        print(f"Access mode : {snapshot['access_mode']}")
    print(f"Period      : {snapshot['period']}")
    print(f"Interval    : {snapshot['display_interval']}")
    print()
    print("Instrument")
    display_market_summary(instrument, aligned_instrument)
    print()
    print("Benchmark")
    display_market_summary(benchmark, aligned_benchmark, show_currency=False)
    print()
    print("Comparison (aligned)")
    print(f"Aligned sessions        : {len(aligned_instrument)}")
    print(f"{instrument['ticker']:<6} period return    : {instrument_return:+.2f}%")
    print(f"{benchmark['ticker']:<6} period return    : {benchmark_return:+.2f}%")
    print(f"Relative performance    : {relative_performance:+.2f} percentage points")
    print()
    print("Base 100")
    print(f"{instrument['ticker']:<6} : {instrument_base_100[0]['value']:.2f} -> {instrument_base_100[-1]['value']:.2f}")
    print(f"{benchmark['ticker']:<6} : {benchmark_base_100[0]['value']:.2f} -> {benchmark_base_100[-1]['value']:.2f}")


if __name__ == "__main__":
    main()