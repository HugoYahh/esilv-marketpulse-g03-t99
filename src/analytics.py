def index_by_date(prices):
    indexed={}
    for row in prices:
        indexed[row["date"]] = row
    return indexed

def align_series(instrument_prices,benchmark_prices):
    instrument_by_date=index_by_date(instrument_prices)
    benchmark_by_date = index_by_date(benchmark_prices)

    common_dates = sorted(set(instrument_by_date)&set(benchmark_by_date))

    aligned_instrument = [instrument_by_date[date] for date in common_dates]
    aligned_benchmark = [benchmark_by_date[date] for date in common_dates]

    return aligned_instrument,aligned_benchmark
    

def calculated_period_return(prices):
    if not prices:
        raise ValueError("Cannot compute a period return on a empty series")

    first_close = float(prices[0]["close"])
    last_close = float(prices[-1]["close"])

    if first_close ==0:
        raise ValueError("First close is zero: period return is undefined.")

    return ((last_close/first_close)-1.0)*100.0


def calculate_base_100 (prices):
    if not prices:
        raise ValueError("Cannot compute a base-100 series on an empty series.")

    first_close = float(prices[0]["close"])

    if first_close ==0:
        raise ValueError("First close is zero: base 100 is undefines.")

    result=[]
    for row in prices:
        value=(float(row["close"])/ first_close)*100.0
        result.append({"date": row["date"], "ticker":row["ticker"], "value": value})
    return result

 
def calculate_relative_performance(instrument_return, benchmark_return):
    return instrument_return - benchmark_return
