import csv
import json
import analytics
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "sample"

PERIOD = "1 month"
INTERVAL = "Daily"
PROVIDER = "Local sample (CSV / JSON)"


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
    
    instruments = load_instruments()
    prices = load_prices()

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    instrument_prices = filter_prices(prices, instrument["ticker"])
    benchmark_prices = filter_prices(prices, benchmark["ticker"])

    print("=== MarketPulse ===")
    print()
    print("Market configuration")
    print(f"Provider : {PROVIDER}")
    print(f"Period   : {PERIOD}")
    print(f"Interval : {INTERVAL}")
    print()
    print("Instrument")
    display_market_summary(instrument, instrument_prices)
    print()
    print("Benchmark")
    display_market_summary(benchmark, benchmark_prices, show_currency=False)

    print(analytics.index_by_date(prices))


if __name__ == "__main__":
    main()