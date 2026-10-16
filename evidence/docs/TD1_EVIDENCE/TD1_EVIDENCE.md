## EVIDENCES FOR TD 1

# pwd, ls, ls -la

![alt text](image.png)

# cd, pwd, ls

![alt text](image-1.png)

# cd ../.., pwd, ls

![alt text](image-2.png)

# cat the data 

![alt text](image-3.png)

Instrument: Apple Inc. (AAPL)
Benchmark: S&P 500 (SP500)
Names and tickers: in `data/sample/instruments.json`, under the `name` and `ticker` keys within the `instrument` and `benchmark` objects.

# head the prices

![alt text](image-4.png)

# grep prices AAPL

![alt text](image-5.png)

# grep prices SP500

![alt text](image-6.png)

What we learn:

- The same file contains both time series, Apple and the S&P 500, and `grep` allows us to separate them.
- Each series has 21 rows, one for each trading day in September 2026.
- The header row does not appear because it contains neither “AAPL” nor “SP500”.

# python and git install 

![alt text](image-7.png)

# launch main code 

![alt text](image-8.png)