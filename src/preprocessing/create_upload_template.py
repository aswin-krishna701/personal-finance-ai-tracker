import pandas as pd
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

# Output folder
TEMPLATE_DIR = BASE_DIR / "data" / "templates"
TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = TEMPLATE_DIR / "user_upload_template.csv"


def create_upload_template():
    print("=" * 80)
    print("CREATING USER UPLOAD CSV TEMPLATE")
    print("=" * 80)

    template_data = [
        {
            "date": "2024-12-01",
            "description": "Salary credited",
            "amount": 45000,
            "type": "Income",
            "category": "Salary",
            "payment_method": "Bank Transfer",
            "merchant": "Company",
            "notes": "Monthly salary"
        },
        {
            "date": "2024-12-02",
            "description": "Zomato food order",
            "amount": 350,
            "type": "Expense",
            "category": "Food",
            "payment_method": "UPI",
            "merchant": "Zomato",
            "notes": "Dinner"
        },
        {
            "date": "2024-12-03",
            "description": "Uber ride",
            "amount": 220,
            "type": "Expense",
            "category": "Travel",
            "payment_method": "Card",
            "merchant": "Uber",
            "notes": "College travel"
        },
        {
            "date": "2024-12-04",
            "description": "Amazon shopping",
            "amount": 1200,
            "type": "Expense",
            "category": "Shopping",
            "payment_method": "Card",
            "merchant": "Amazon",
            "notes": "Headphones"
        },
        {
            "date": "2024-12-05",
            "description": "Netflix subscription",
            "amount": 199,
            "type": "Expense",
            "category": "Subscriptions",
            "payment_method": "Card",
            "merchant": "Netflix",
            "notes": "Monthly plan"
        }
    ]

    df = pd.DataFrame(template_data)
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Upload template saved to: {OUTPUT_FILE}")
    print("\nTemplate Preview:")
    print(df)

    print("\nCSV upload template created successfully.")


if __name__ == "__main__":
    create_upload_template()