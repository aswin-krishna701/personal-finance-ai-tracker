import pandas as pd
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

# Input file
CLEANED_FILE = BASE_DIR / "data" / "processed" / "personal_finance_cleaned.csv"

# Output folder
REPORTS_DIR = BASE_DIR / "outputs" / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

BUDGET_REPORT_FILE = REPORTS_DIR / "budget_report.csv"


# Fixed monthly/category budgets
CATEGORY_BUDGETS = {
    "Food": 6000,
    "Travel": 3000,
    "Shopping": 5000,
    "Bills": 8000,
    "Entertainment": 2500,
    "Education": 4000,
    "Health": 3000,
    "Subscriptions": 1500,
    "Others": 3000
}


def get_alert_status(usage_percentage):
    """
    Return budget alert status based on usage percentage.
    """
    if usage_percentage < 70:
        return "Safe"
    elif usage_percentage < 90:
        return "Warning"
    elif usage_percentage <= 100:
        return "Near Limit"
    else:
        return "Over Budget"


def run_budget_tracking():
    print("=" * 80)
    print("RUNNING BUDGET TRACKING MODULE")
    print("=" * 80)

    if not CLEANED_FILE.exists():
        print(f"ERROR: File not found: {CLEANED_FILE}")
        print("Run Phase 4 first: clean_personal_finance.py")
        return

    df = pd.read_csv(CLEANED_FILE)

    print(f"Loaded cleaned dataset shape: {df.shape}")

    # Use only expenses
    expense_df = df[df["type"] == "Expense"].copy()

    if expense_df.empty:
        print("No expense data found.")
        return

    # Calculate total spent by category
    category_spending = expense_df.groupby("category")["amount"].sum().reset_index()
    category_spending = category_spending.rename(columns={"amount": "actual_spent"})

    budget_rows = []

    for category, budget_amount in CATEGORY_BUDGETS.items():
        spent_value = category_spending.loc[
            category_spending["category"] == category,
            "actual_spent"
        ]

        actual_spent = float(spent_value.iloc[0]) if not spent_value.empty else 0.0
        remaining_budget = budget_amount - actual_spent

        usage_percentage = 0
        if budget_amount > 0:
            usage_percentage = (actual_spent / budget_amount) * 100

        alert_status = get_alert_status(usage_percentage)

        budget_rows.append({
            "category": category,
            "budget_amount": round(budget_amount, 2),
            "actual_spent": round(actual_spent, 2),
            "remaining_budget": round(remaining_budget, 2),
            "budget_usage_percentage": round(usage_percentage, 2),
            "alert_status": alert_status
        })

    budget_report = pd.DataFrame(budget_rows)

    # Sort by highest budget usage
    budget_report = budget_report.sort_values(
        "budget_usage_percentage",
        ascending=False
    ).reset_index(drop=True)

    # Save report
    budget_report.to_csv(BUDGET_REPORT_FILE, index=False)

    print(f"Budget report saved to: {BUDGET_REPORT_FILE}")

    print("\nBudget Report:")
    print(budget_report)

    print("\nBudget tracking completed successfully.")


if __name__ == "__main__":
    run_budget_tracking()
    