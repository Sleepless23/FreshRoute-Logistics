# ROLE FOR: RENZ SALTA
# Optional for reports
# Contains utility functions for exporting data to CSV files or excel

import csv
from datetime import datetime


def export_to_csv(rows: list[dict], filename_prefix: str) -> str:
    if not rows:
        raise ValueError("No data to export")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.csv"

    fieldnames = list(rows[0].keys())
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    return filename
