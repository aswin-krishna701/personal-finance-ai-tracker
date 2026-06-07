import pandas as pd
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

# Input and output paths
RAW_FILE = BASE_DIR / "data" / "raw" / "User0_credit_card_transactions.csv"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
OUTPUT_FILE = PROCESSED_DIR / "card_transactions_cleaned.csv"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def clean_amount(value):
    """
    Convert amount like '$-12.45' or '$45.20' into positive numeric value.
    For this project, all card transactions are treated as expenses.
    """
    if pd.isna(value):
        return None

    value = str(value).replace("$", "").replace(",", "").strip()

    try:
        return abs(float(value))
    except ValueError:
        return None


def clean_credit_card():
    print("=" * 80)
    print("CLEANING CREDIT CARD DATASET")
    print("=" * 80)

    if not RAW_FILE.exists():
        print(f"ERROR: File not found: {RAW_FILE}")
        return

    # Load dataset
    df = pd.read_csv(RAW_FILE)

    print(f"Original shape: {df.shape}")

    # Rename columns
    df = df.rename(columns={
        "Year": "year",
        "Month": "month_number",
        "Day": "day",
        "Time": "time",
        "Amount": "amount",
        "Merchant Name": "merchant",
        "Merchant City": "merchant_city",
        "Merchant State": "merchant_state",
        "MCC": "mcc",
        "Errors?": "errors",
        "Is Fraud?": "is_fraud",
        "Use Chip": "use_chip",
        "Card": "card"
    })

    # Create date column correctly
    df["date"] = pd.to_datetime({
        "year": df["year"],
        "month": df["month_number"],
        "day": df["day"]
    }, errors="coerce")

    # Clean amount
    df["amount"] = df["amount"].apply(clean_amount)

    # Remove rows with missing date or amount
    df = df.dropna(subset=["date", "amount"])

    # Treat all card transactions as Expense
    df["type"] = "Expense"

    # Merchant is numeric in this dataset, so convert to readable ID
    df["merchant"] = df["merchant"].astype(str)
    df["merchant"] = "Merchant_" + df["merchant"]

    # Use MCC as category for now
    df["category"] = "MCC_" + df["mcc"].astype(str)

    # Create description
    df["description"] = df["merchant"] + " transaction"

    # Clean fraud column
    df["is_fraud"] = df["is_fraud"].astype(str).str.strip().str.title()

    # Fill optional missing values
    df["merchant_city"] = df["merchant_city"].fillna("Unknown")
    df["merchant_state"] = df["merchant_state"].fillna("Unknown")
    df["errors"] = df["errors"].fillna("No Error")

    # Date-based columns
    df["month"] = df["date"].dt.month_name()
    df["year"] = df["date"].dt.year
    df["day_name"] = df["date"].dt.day_name()

    # Sort and add transaction ID
    df = df.sort_values(["date", "time"]).reset_index(drop=True)
    df.insert(0, "transaction_id", range(1, len(df) + 1))

    # Final columns
    final_columns = [
        "transaction_id",
        "date",
        "time",
        "type",
        "category",
        "description",
        "amount",
        "merchant",
        "merchant_city",
        "merchant_state",
        "mcc",
        "use_chip",
        "errors",
        "is_fraud",
        "month",
        "year",
        "day_name"
    ]

    df = df[final_columns]

    # Save cleaned dataset
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Cleaned shape: {df.shape}")
    print(f"Cleaned file saved to: {OUTPUT_FILE}")

    print("\nFirst 5 cleaned rows:")
    print(df.head())

    print("\nFraud count:")
    print(df["is_fraud"].value_counts())

    print("\nTop 10 MCC categories:")
    print(df["category"].value_counts().head(10))

    print("\nAmount summary:")
    print(df["amount"].describe())


if __name__ == "__main__":
    clean_credit_card()