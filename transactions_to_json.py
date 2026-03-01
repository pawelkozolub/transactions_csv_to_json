#!/usr/bin/env python3
"""Convert transactions.csv to JSON (list of dicts keyed by headers)."""

import argparse
import csv
import io
import json
import sys


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
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        lines = f.readlines()
    # Skip leading blank lines
    start = 0
    while start < len(lines) and not lines[start].strip():
        start += 1
    reader = csv.DictReader(io.StringIO("".join(lines[start:])), delimiter=";")
    data = list(reader)

    output_path = args.output or args.input.replace(".csv", ".json").replace(".CSV", ".json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(data)} records to {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
