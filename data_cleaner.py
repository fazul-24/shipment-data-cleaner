"""
Shipment Data Cleaner
----------------------
Cleans a messy shipment/export dataset (CSV) commonly seen in
logistics/operations work: duplicate rows, missing values, inconsistent
text casing/spacing, and invalid numeric values.

Usage:
    python data_cleaner.py sample_shipments.csv cleaned_shipments.csv
"""

import sys
import pandas as pd


def load_data(input_path: str) -> pd.DataFrame:
    """Read the raw CSV into a DataFrame."""
    return pd.read_csv(input_path)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Apply a series of cleaning steps and return a clean DataFrame."""

    report = {}

    # 1. Drop exact duplicate rows
    before = len(df)
    df = df.drop_duplicates()
    report["duplicates_removed"] = before - len(df)

    # 2. Drop rows with no ShipmentID (can't track these records)
    before = len(df)
    df = df.dropna(subset=["ShipmentID"])
    report["rows_without_id_removed"] = before - len(df)

    # 3. Standardize text columns: strip whitespace (leave NA as NA for now)
    text_cols = ["Customer", "Origin", "Destination"]
    for col in text_cols:
        df[col] = df[col].str.strip()

    # 4. Standardize the Status column (title case, fill missing as "Unknown")
    df["Status"] = df["Status"].str.strip().str.title()
    df["Status"] = df["Status"].fillna("Unknown")

    # 5. Fix invalid weights: negative weights are impossible, treat as missing
    df.loc[df["Weight_KG"] < 0, "Weight_KG"] = pd.NA

    # 6. Fill missing weights with the average weight (simple imputation)
    avg_weight = df["Weight_KG"].mean()
    missing_weights = df["Weight_KG"].isna().sum()
    df["Weight_KG"] = df["Weight_KG"].fillna(round(avg_weight, 1))
    report["weights_filled"] = int(missing_weights)

    # 7. Fill missing destination/customer with "Unknown" so downstream
    #    reports don't break on NaN
    df["Customer"] = df["Customer"].fillna("Unknown")
    df["Destination"] = df["Destination"].fillna("Unknown")

    df = df.reset_index(drop=True)

    print("\n--- Cleaning Report ---")
    for key, value in report.items():
        print(f"{key.replace('_', ' ').capitalize()}: {value}")
    print("-----------------------\n")

    return df


def main():
    if len(sys.argv) != 3:
        print("Usage: python data_cleaner.py <input_csv> <output_csv>")
        sys.exit(1)

    input_path, output_path = sys.argv[1], sys.argv[2]

    df = load_data(input_path)
    print(f"Loaded {len(df)} rows from {input_path}")

    cleaned_df = clean_data(df)
    cleaned_df.to_csv(output_path, index=False)
    print(f"Saved {len(cleaned_df)} clean rows to {output_path}")


if __name__ == "__main__":
    main()
