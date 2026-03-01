#!/usr/bin/env python3
"""Convert transactions.csv to JSON (list of dicts keyed by headers)."""

import argparse
import csv
import io
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_STOCK_TICKERS_PATH = SCRIPT_DIR / "stock_tickers.json"
MIN_COMMISSION = 5.0


def load_stock_tickers(path: Path | None = None) -> dict[tuple[str, str], str]:
    """Load (Gielda, Papier) -> Ticker mapping from JSON file."""
    path = path or DEFAULT_STOCK_TICKERS_PATH
    with open(path, "r", encoding="utf-8") as f:
        raw: dict[str, dict[str, str]] = json.load(f)
    return {
        (gielda, papier): ticker
        for gielda, papers in raw.items()
        for papier, ticker in papers.items()
    }


def _parse_price(s: str) -> float:
    """Parse European decimal format (e.g. '157,40') to float."""
    return float(s.replace(",", ".")) if s else 0.0


def _parse_number(s: str) -> int:
    """Parse integer string (e.g. '7') to int."""
    return int(float(s)) if s else 0


def _build_output_record(row: dict[str, str], min_commission: float) -> dict:
    """Build output dict with keys in specified order."""
    number = _parse_number(row.get("Liczba zrealizowana", ""))
    price = _parse_price(row.get("Limit ceny", ""))
    order_value = round(number * price, 2)
    commission = max(round(order_value * 0.0039, 2), min_commission)

    k_s = row.get("K/S", "")
    order = "BUY" if k_s == "K" else "SELL"

    return {
        "Date": row.get("Data zlecenia", ""),
        "Order": order,
        "Market": row.get("Gielda", ""),
        "Ticker": row.get("Ticker", ""),
        "Asset": row.get("Papier", ""),
        "Shares": number,
        "Price": price,
        "Order value": order_value,
        "Commission": commission,
    }


def get_stock_ticker(
    papier: str, gielda: str, stock_tickers: dict[tuple[str, str], str]
) -> str:
    """Return 3-letter stock ticker for the given Papier on the given Gielda (exchange)."""
    key = (gielda, papier)
    if key not in stock_tickers:
        raise ValueError(
            f"Unknown stock: Papier={papier!r} on Gielda={gielda!r}. "
            f"Add it to stock_tickers.json"
        )
    return stock_tickers[key]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert transactions CSV to JSON."
    )
    parser.add_argument(
        "input",
        nargs="?",
        default="transactions.csv",
        help="Input transactions CSV path (default: transactions.csv)",
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="FILE",
        default=None,
        help="Output JSON path (default: transactions.json)",
    )
    parser.add_argument(
        "-c",
        "--stock-tickers",
        metavar="FILE",
        default=None,
        help="Stock ticker mapping JSON path (default: stock_tickers.json beside script)",
    )
    parser.add_argument(
        "--min-commission",
        type=float,
        default=MIN_COMMISSION,
        help="Minimum commission in PLN (default: 5.0)",
    )
    args = parser.parse_args()

    stock_tickers = load_stock_tickers(
        Path(args.stock_tickers) if args.stock_tickers else None
    )

    with open(args.input, "r", encoding="utf-8") as f:
        lines = f.readlines()
    # Skip leading blank lines
    start = 0
    while start < len(lines) and not lines[start].strip():
        start += 1
    reader = csv.DictReader(io.StringIO("".join(lines[start:])), delimiter=";")
    data = []
    for row in reader:
        if row.get("Stan") != "Zrealizowane":
            continue
        papier = row.get("Papier", "")
        gielda = row.get("Gielda", "")
        row["Ticker"] = get_stock_ticker(papier, gielda, stock_tickers)
        data.append(_build_output_record(row, args.min_commission))

    output_path = args.output or args.input.replace(".csv", ".json").replace(".CSV", ".json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(data)} records to {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
