import pandas as pd
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

# Dataset paths
PERSONAL_FINANCE_FILE = BASE_DIR / "data" / "raw" / "Personal_Finance_Dataset.csv"
CARD_FILE = BASE_DIR / "data" / "raw" / "User0_credit_card_transactions.csv"

# Output folder
REPORTS_DIR = BASE_DIR / "outputs" / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def inspect_dataset(file_path, dataset_name):
    print("\n" + "=" * 80)
    print(f"INSPECTING DATASET: {dataset_name}")
    print("=" * 80)

    if not file_path.exists():
        print(f"ERROR: File not found: {file_path}")
        return

    # Load dataset
    df = pd.read_csv(file_path)

    print("\n1. Dataset Shape")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print("\n2. Column Names")
    print(list(df.columns))

    print("\n3. First 5 Rows")
    print(df.head())

    print("\n4. Data Types")
    print(df.dtypes)

    print("\n5. Missing Values")
    print(df.isnull().sum())

    print("\n6. Duplicate Rows")
    print(df.duplicated().sum())

    print("\n7. Basic Numeric Summary")
    print(df.describe(include="all"))

    # Save report as CSV
    summary = pd.DataFrame({
        "column_name": df.columns,
        "data_type": df.dtypes.astype(str).values,
        "missing_values": df.isnull().sum().values,
        "unique_values": df.nunique().values
    })

    output_file = REPORTS_DIR / f"{dataset_name}_inspection_report.csv"
    summary.to_csv(output_file, index=False)

    print(f"\nInspection report saved to: {output_file}")


def main():
    inspect_dataset(PERSONAL_FINANCE_FILE, "personal_finance")
    inspect_dataset(CARD_FILE, "credit_card")


if __name__ == "__main__":
    main()