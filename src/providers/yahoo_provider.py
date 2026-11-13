import yfinance as yf

CANONICAL_TO_YAHOO = {
    "AAPL": "AAPL",
    "SP500": "^GSPC",  
}


def fetch_yahoo_prices(canonical_ticker: str, lookback: str, interval: str):
    if canonical_ticker not in CANONICAL_TO_YAHOO:
        raise ValueError(f"Ticker {canonical_ticker} not supported by Yahoo provider")
    yahoo_ticker = CANONICAL_TO_YAHOO[canonical_ticker]

    raw_yahoo_data = yf.download(
        yahoo_ticker,
        period=lookback,
        interval=interval,
        multi_level_index=False,  
        progress=False,           
    )

    rows = []

    for date, row in raw_yahoo_data.iterrows():
        dic = {
            "date": date.strftime("%Y-%m-%d"),  
            "ticker": canonical_ticker,         
            "open": float(row["Open"]),        
            "high": float(row["High"]),
            "low": float(row["Low"]),
            "close": float(row["Close"]),
            "volume": int(row["Volume"]),       
        }
        rows.append(dic)
    sorted_rows = sorted(rows, key=lambda dico: dico["date"])
    return sorted_rows


if __name__ == "__main__":
    rows = fetch_yahoo_prices("SP500", "1mo", "1d")
    for row in rows:
        print(row)