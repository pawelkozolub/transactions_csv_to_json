# CSV to JSON Converter

## Summary

A minimal Python CLI that converts transactions CSV to JSON as a list of dictionaries, where each dictionary maps CSV column headers to row values. The `transactions_to_json.py` script is responsible only for transaction conversion.

### Implemented Features

- **CSV parsing**: Uses `csv.DictReader` with semicolon (`;`) delimiter and UTF-8 encoding
- **Leading blank lines**: Automatically skips empty lines at the start of the file
- **Output format**: JSON array of objects; each row becomes a dict with headers as keys and cell values as values
- **Code field**: Each record gets a `Code` key with the official 3-letter ticker prescribed by the stock exchange (`Gielda`). Codes are hardcoded in `STOCK_CODE_MAP` from GPW/TradingView sources; add entries for new stocks.
- **CLI arguments**:
  - `input` (optional): Input CSV path (default: `transactions.csv`)
  - `-o`, `--output`: Output JSON path (default: derived from input, e.g. `transactions.json`)

### Dependencies

Standard library only: `csv`, `json`, `argparse`, `io`

### Usage

```bash
python transactions_to_json.py                          # transactions.csv → transactions.json
python transactions_to_json.py transactions.csv         # same
python transactions_to_json.py transactions.csv -o result.json  # custom output
```

### Output Example

```json
[
  {
    "Stan": "Zrealizowane",
    "Papier": "DIGITANET",
    "Gielda": "WWA-GPW",
    "Code": "DIG",
    "K/S": "K",
    "Liczba zlecona": "7",
    "Liczba zrealizowana": "7",
    "Limit ceny": "157,40",
    "Waluta": "PLN",
    "Limit aktywacji": "",
    "Data zlecenia": "27.02.2026 12:39:25"
  }
]
```
