from __future__ import annotations

import csv
from pathlib import Path


def export_csv(rows: list[dict[str, str]], output_file: str) -> None:
    output = Path(output_file)
    output.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = ["account_id", "account_name", "user_name", "arn", "created"]
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
