import pandas as pd
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

# Input file
CLEANED_FILE = BASE_DIR / "data" / "processed" / "personal_finance_cleaned.csv"

# Output folder
SAMPLE_DIR = BASE_DIR / "data" / "sample"
SAMPLE_DIR.mkdir(parents=True, exist_ok=True)

SMALL_SAMPLE_FILE = SAMPLE_DIR / "small_sample_transactions.csv"
MEDIUM_DEMO_FILE = SAMPLE_DIR / "medium_demo_transactions.csv"


def create_sample_datasets():
    print("=" * 80)
    print("CREATING SMALL AND MEDIUM SAMPLE DATASETS")
    print("=" * 80)

    if not CLEANED_FILE.exists():
        print(f"ERROR: File not found: {CLEANED_FILE}")
        print("Run Phase 4 first: clean_personal_finance.py")
        return

    df = pd.read_csv(CLEANED_FILE)

    print(f"Loaded cleaned dataset shape: {df.shape}")

    # Convert date to datetime
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    # Sort by date
    df = df.sort_values("date").reset_index(drop=True)

    # Small dataset: first 200 rows
    small_df = df.head(200)

    # Medium dataset: first 1500 rows or full dataset if less than 1500
    medium_df = df.head(min(1500, len(df)))

    # Save outputs
    small_df.to_csv(SMALL_SAMPLE_FILE, index=False)
    medium_df.to_csv(MEDIUM_DEMO_FILE, index=False)

    print(f"Small sample saved to: {SMALL_SAMPLE_FILE}")
    print(f"Small sample shape: {small_df.shape}")
    print(f"Small sample date range: {small_df['date'].min()} to {small_df['date'].max()}")

    print(f"\nMedium demo saved to: {MEDIUM_DEMO_FILE}")
    print(f"Medium demo shape: {medium_df.shape}")
    print(f"Medium demo date range: {medium_df['date'].min()} to {medium_df['date'].max()}")

    print("\nFiles created successfully.")


if __name__ == "__main__":
    create_sample_datasets()