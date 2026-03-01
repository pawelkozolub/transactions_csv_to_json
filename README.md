# CSV to JSON Converter

## Summary

A minimal Python CLI that converts transactions CSV to JSON as a list of dictionaries, where each dictionary maps CSV column headers to row values. The `transactions_to_json.py` script is responsible only for transaction conversion.

### Implemented Features

- **CSV parsing**: Uses `csv.DictReader` with semicolon (`;`) delimiter and UTF-8 encoding
- **Leading blank lines**: Automatically skips empty lines at the start of the file
- **Output format**: JSON array of objects; each row becomes a dict with headers as keys and cell values as values
- **Ticker field**: Each record gets a `Ticker` key with the official 3-letter ticker prescribed by the stock exchange (`Gielda`). Tickers are loaded from external `stock_tickers.json`. Raises an error if a stock (Papier) is not in the mapping.
- **CLI arguments**:
  - `input` (optional): Input CSV path (default: `transactions.csv`)
  - `-o`, `--output`: Output JSON path (default: derived from input, e.g. `transactions.json`)
  - `-c`, `--stock-tickers`: Stock ticker mapping JSON path
  - `--min-commission`: Minimum commission in PLN (default: 5.0)

### Files

- `stock_tickers.json` — exchange (Gielda) → Papier → 3-letter ticker mapping. Edit to add new stocks.

### Dependencies

Standard library only: `csv`, `json`, `argparse`, `io`

### Usage

```bash
python transactions_to_json.py                          # transactions.csv → transactions.json
python transactions_to_json.py transactions.csv         # same
python transactions_to_json.py transactions.csv -o result.json  # custom output
python transactions_to_json.py -c my_tickers.json               # custom stock ticker mapping
```

### Output Example

```json
[
  {
    "Date": "27.02.2026 12:39:25",
    "Order": "BUY",
    "Market": "WWA-GPW",
    "Ticker": "DIG",
    "Asset": "DIGITANET",
    "Shares": 7,
    "Price": 157.4,
    "Order value": 1101.8,
    "Commission": 5.0
  }
]
```

- **Order value**: Shares × Price
- **Commission**: max((Order value × 0.39%), 5.0 PLN). Override minimum with `--min-commission`
