import pandas as pd
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

# Default test input and output
TEMPLATE_FILE = BASE_DIR / "data" / "templates" / "user_upload_template.csv"
OUTPUT_DIR = BASE_DIR / "outputs" / "cleaned_data"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "uploaded_transactions_cleaned.csv"


REQUIRED_COLUMNS = [
    "date",
    "description",
    "amount",
    "type",
    "category"
]

OPTIONAL_COLUMNS = [
    "payment_method",
    "merchant",
    "notes"
]


def auto_categorize(description):
    """
    Auto-categorize transaction using simple keyword rules.
    Used when category is missing.
    """
    description = str(description).lower()

    food_keywords = ["zomato", "swiggy", "restaurant", "food", "cafe", "hotel"]
    travel_keywords = ["uber", "ola", "bus", "train", "petrol", "fuel", "taxi"]
    shopping_keywords = ["amazon", "flipkart", "myntra", "shopping", "store"]
    bills_keywords = ["electricity", "recharge", "internet", "water", "bill", "rent"]
    subscriptions_keywords = ["netflix", "spotify", "prime", "subscription"]
    income_keywords = ["salary", "freelance", "credited", "income"]

    if any(word in description for word in food_keywords):
        return "Food"
    elif any(word in description for word in travel_keywords):
        return "Travel"
    elif any(word in description for word in shopping_keywords):
        return "Shopping"
    elif any(word in description for word in bills_keywords):
        return "Bills"
    elif any(word in description for word in subscriptions_keywords):
        return "Subscriptions"
    elif any(word in description for word in income_keywords):
        return "Salary"
    else:
        return "Others"


def classify_need_or_want(category, transaction_type):
    if transaction_type == "Income":
        return "Income"

    need_categories = ["Bills", "Health", "Education", "Food", "Travel"]
    want_categories = ["Shopping", "Entertainment", "Subscriptions"]

    if category in need_categories:
        return "Need"
    elif category in want_categories:
        return "Want"
    else:
        return "Other"


def clean_uploaded_csv(input_file=TEMPLATE_FILE, output_file=OUTPUT_FILE):
    print("=" * 80)
    print("CLEANING USER UPLOADED CSV")
    print("=" * 80)

    input_file = Path(input_file)

    if not input_file.exists():
        print(f"ERROR: File not found: {input_file}")
        return None

    df = pd.read_csv(input_file)

    print(f"Original uploaded shape: {df.shape}")

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Check required columns
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]

    if missing_columns:
        print(f"ERROR: Missing required columns: {missing_columns}")
        print(f"Required columns are: {REQUIRED_COLUMNS}")
        return None

    # Add optional columns if missing
    for col in OPTIONAL_COLUMNS:
        if col not in df.columns:
            df[col] = "Unknown"

    # Convert date
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Convert amount
    df["amount"] = (
        df["amount"]
        .astype(str)
        .str.replace("₹", "", regex=False)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    # Remove invalid rows
    df = df.dropna(subset=["date", "amount"])

    # Clean type
    df["type"] = df["type"].astype(str).str.strip().str.title()
    df = df[df["type"].isin(["Income", "Expense"])]

    # Clean description
    df["description"] = df["description"].astype(str).str.strip()

    # Fill missing category using keyword rules
    df["category"] = df["category"].fillna("")
    df["category"] = df.apply(
        lambda row: auto_categorize(row["description"])
        if str(row["category"]).strip() == ""
        else str(row["category"]).strip().title(),
        axis=1
    )

    # Fill optional values
    df["payment_method"] = df["payment_method"].fillna("Unknown").astype(str).str.strip()
    df["merchant"] = df["merchant"].fillna("Unknown").astype(str).str.strip()
    df["notes"] = df["notes"].fillna("").astype(str).str.strip()

    # Add need/want
    df["need_or_want"] = df.apply(
        lambda row: classify_need_or_want(row["category"], row["type"]),
        axis=1
    )

    # Date columns
    df["month"] = df["date"].dt.month_name()
    df["year"] = df["date"].dt.year
    df["day_name"] = df["date"].dt.day_name()

    # Sort and transaction id
    df = df.sort_values("date").reset_index(drop=True)
    df.insert(0, "transaction_id", range(1, len(df) + 1))

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
        "notes",
        "month",
        "year",
        "day_name"
    ]

    df = df[final_columns]

    df.to_csv(output_file, index=False)

    print(f"Cleaned uploaded shape: {df.shape}")
    print(f"Cleaned uploaded CSV saved to: {output_file}")

    print("\nCleaned Upload Preview:")
    print(df.head())

    print("\nUser uploaded CSV cleaning completed successfully.")

    return df


if __name__ == "__main__":
    clean_uploaded_csv()