# Shipment Data Cleaner

A Python script that cleans messy shipment/export data — the kind of
data issues commonly seen in logistics and operations work (duplicate
records, missing fields, inconsistent text casing, invalid values).

## What it does

Given a raw CSV of shipment records, the script:

- Removes exact duplicate rows
- Drops rows with no Shipment ID (untrackable records)
- Strips extra whitespace from text fields (Customer, Origin, Destination)
- Standardizes the `Status` column casing (e.g. `delivered`, `DELIVERED` → `Delivered`)
- Replaces impossible values (e.g. negative weight) with missing, then
  fills missing weights using the average weight
- Fills missing Customer/Destination/Status with `"Unknown"` so the
  data is safe for downstream reporting
- Prints a short cleaning report (how many duplicates removed, how many
  weights filled, etc.)

## Tech used

- Python 3
- pandas

## How to run

```bash
pip install pandas
python data_cleaner.py sample_shipments.csv cleaned_shipments.csv
```

This reads `sample_shipments.csv` (included, with intentionally messy
sample data), cleans it, prints a report to the console, and writes the
cleaned result to `cleaned_shipments.csv`.

## Example output

```
Loaded 10 rows from sample_shipments.csv

--- Cleaning Report ---
Duplicates removed: 1
Rows without id removed: 1
Weights filled: 2
-----------------------

Saved 8 clean rows to cleaned_shipments.csv
```

## Why this project

Built to demonstrate applying Python/pandas to real-world data quality
problems similar to what comes up in shipment/export documentation
work — duplicate records, missing fields, and inconsistent formatting.
