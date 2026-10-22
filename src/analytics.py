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
    raise NotImplementedError # Owner : Chloe

def calculate_base_100 (prices):
    raise NotImplementedError # Owner Chloe

def calculate_relative_performance(instrument_return, benchmark_return):
    raise NotImplementedError # Owner Chloe

