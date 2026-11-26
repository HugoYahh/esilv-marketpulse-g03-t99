# Bloomberg Field Mapping

## Access mode

APPROVED_SAMPLE

Source:
data/sample/bloomberg_reference_sample.json

Reference:
docs/10_BLOOMBERG_INSTRUCTOR_REFERENCE.md

Live connectivity:
not demonstrated

## Market instruments

| Role | Canonical ticker | Bloomberg identifier |
|---|---|---|
| Instrument | AAPL | AAPL US Equity |
| Benchmark | SP500 | SPX Index |

## Field mapping

Note: `observation_date`, `open_value`, `high_value`, `low_value`, `close_value`, and `volume_value` are teaching wrapper keys from the fallback fixture (`teaching wrapper key != Bloomberg LIVE field mnemonic`).

| MarketPulse field | Source field or mapping | Status / notes |
|---|---|---|
| date | observation_date | teaching wrapper key (YYYY-MM-DD) |
| ticker | application mapping | AAPL or SP500 (canonical ticker preserved) |
| open | open_value | teaching wrapper key |
| high | high_value | teaching wrapper key |
| low | low_value | teaching wrapper key |
| close | close_value | teaching wrapper key |
| volume | volume_value | teaching wrapper key (0 for SPX Index) |

## TD10 handoff

- Access mode: APPROVED_SAMPLE
- Instrument identifier: AAPL US Equity -> AAPL
- Benchmark identifier: SPX Index -> SP500
- Date representation: ISO string `YYYY-MM-DD` (`observation_date`)
- Input structure: JSON object with `series` array (2 entries: instrument and benchmark), each containing `canonical_ticker`, `provider_identifier`, and `observations` list
- Missing fields: none (all 6 teaching wrapper keys present; `volume_value` is `0` on `SPX Index`)
- Special normalization notes: flatten `series[].observations[]` into canonical rows (`date`, `ticker`, `open`, `high`, `low`, `close`, `volume`) and preserve canonical tickers `AAPL` and `SP500`

Expected canonical reference:
data/sample/bloomberg_reference_expected.json