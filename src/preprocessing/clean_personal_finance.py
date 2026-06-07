import pandas as pd
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

# Input and output paths
RAW_FILE = BASE_DIR / "data" / "raw" / "Personal_Finance_Dataset.csv"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
OUTPUT_FILE = PROCESSED_DIR / "personal_finance_cleaned.csv"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def standardize_category(category):
    """
    Convert category names into clean and consistent format.
    """
    if pd.isna(category):
        return "Others"

    category = str(category).strip().lower()

    category_mapping = {
        "food & drink": "Food",
        "food": "Food",
        "groceries": "Food",

        "utilities": "Bills",
        "rent": "Bills",
        "bills": "Bills",

        "transport": "Travel",
        "travel": "Travel",

        "shopping": "Shopping",

        "entertainment": "Entertainment",

        "health": "Health",
        "medical": "Health",
        "health & fitness": "Health",
        "fitness": "Health",

        "education": "Education",

        "investment": "Investment",
        "salary": "Salary",
        "income": "Income",

        "others": "Others",
        "other": "Others"
    }

    return category_mapping.get(category, category.title())


def classify_need_or_want(category, transaction_type):
    """
    Classify expense as Need or Want.
    Income is marked as Income.
    """
    if transaction_type == "Income":
        return "Income"

    need_categories = ["Bills", "Health", "Education", "Food", "Travel"]
    want_categories = ["Shopping", "Entertainment"]

    if category in need_categories:
        return "Need"
    elif category in want_categories:
        return "Want"
    else:
        return "Other"


def clean_personal_finance():
    print("=" * 80)
    print("CLEANING PERSONAL FINANCE DATASET")
    print("=" * 80)

    if not RAW_FILE.exists():
        print(f"ERROR: File not found: {RAW_FILE}")
        return

    # Load dataset
    df = pd.read_csv(RAW_FILE)

    print(f"Original shape: {df.shape}")

    # Rename columns
    df = df.rename(columns={
        "Date": "date",
        "Transaction Description": "description",
        "Category": "category",
        "Amount": "amount",
        "Type": "type"
    })

    # Convert date
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Convert amount
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    # Remove duplicates
    df = df.drop_duplicates()

    # Remove rows with missing important values
    df = df.dropna(subset=["date", "amount"])

    # Standardize type
    df["type"] = df["type"].astype(str).str.strip().str.title()

    # Keep only valid transaction types
    df = df[df["type"].isin(["Income", "Expense"])]

    # Standardize category
    df["category"] = df["category"].apply(standardize_category)

    # Fix inconsistent category/type combinations from synthetic dataset
    income_categories = ["Salary", "Investment", "Income"]

    # If transaction is Income, keep income-related category or convert to Income
    df.loc[
        (df["type"] == "Income") & (~df["category"].isin(income_categories)),
        "category"
    ] = "Income"

    # If transaction is Expense but category is Salary or Investment, convert it to Others
    df.loc[
        (df["type"] == "Expense") & (df["category"].isin(["Salary", "Investment"])),
        "category"
    ] = "Others"

    # Add missing useful columns
    df["payment_method"] = "Unknown"
    df["merchant"] = "Unknown"

    # Add need_or_want column
    df["need_or_want"] = df.apply(
        lambda row: classify_need_or_want(row["category"], row["type"]),
        axis=1
    )

    # Add date-based columns
    df["month"] = df["date"].dt.month_name()
    df["year"] = df["date"].dt.year
    df["day_name"] = df["date"].dt.day_name()

    # Add transaction id
    df = df.sort_values("date").reset_index(drop=True)
    df.insert(0, "transaction_id", range(1, len(df) + 1))

    # Final column order
    final_columns = [
        "transaction_id",
        "date",
        "type",
        "category",
        "description",
        "amount",
        "payment_method",
        "need_or_want",
        "merchant",
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

    print("\nCategory count:")
    print(df["category"].value_counts())

    print("\nType count:")
    print(df["type"].value_counts())

    print("\nNeed vs Want count:")
    print(df["need_or_want"].value_counts())


if __name__ == "__main__":
    clean_personal_finance()