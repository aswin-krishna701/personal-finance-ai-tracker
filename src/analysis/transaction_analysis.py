import pandas as pd
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

# Input file
CLEANED_FILE = BASE_DIR / "data" / "processed" / "personal_finance_cleaned.csv"

# Output folder
REPORTS_DIR = BASE_DIR / "outputs" / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

FINANCE_SUMMARY_FILE = REPORTS_DIR / "finance_summary.csv"
MONTHLY_SUMMARY_FILE = REPORTS_DIR / "monthly_summary.csv"
CATEGORY_SUMMARY_FILE = REPORTS_DIR / "category_summary.csv"


def calculate_finance_summary(df):
    income_df = df[df["type"] == "Income"]
    expense_df = df[df["type"] == "Expense"]

    total_income = income_df["amount"].sum()
    total_expense = expense_df["amount"].sum()
    total_savings = total_income - total_expense

    savings_rate = 0
    if total_income > 0:
        savings_rate = (total_savings / total_income) * 100

    average_daily_spending = expense_df.groupby("date")["amount"].sum().mean()

    highest_expense = expense_df["amount"].max()
    lowest_expense = expense_df["amount"].min()

    if not expense_df.empty:
        top_spending_category = expense_df.groupby("category")["amount"].sum().idxmax()
    else:
        top_spending_category = "None"

    need_spending = expense_df[expense_df["need_or_want"] == "Need"]["amount"].sum()
    want_spending = expense_df[expense_df["need_or_want"] == "Want"]["amount"].sum()
    other_spending = expense_df[expense_df["need_or_want"] == "Other"]["amount"].sum()

    summary = {
        "total_income": round(total_income, 2),
        "total_expense": round(total_expense, 2),
        "total_savings": round(total_savings, 2),
        "savings_rate_percent": round(savings_rate, 2),
        "average_daily_spending": round(average_daily_spending, 2),
        "highest_expense": round(highest_expense, 2),
        "lowest_expense": round(lowest_expense, 2),
        "top_spending_category": top_spending_category,
        "need_spending": round(need_spending, 2),
        "want_spending": round(want_spending, 2),
        "other_spending": round(other_spending, 2),
        "total_transactions": len(df),
        "income_transactions": len(income_df),
        "expense_transactions": len(expense_df)
    }

    return pd.DataFrame([summary])


def calculate_monthly_summary(df):
    monthly = df.groupby(["year", "month", "type"])["amount"].sum().reset_index()

    monthly_pivot = monthly.pivot_table(
        index=["year", "month"],
        columns="type",
        values="amount",
        fill_value=0
    ).reset_index()

    if "Income" not in monthly_pivot.columns:
        monthly_pivot["Income"] = 0

    if "Expense" not in monthly_pivot.columns:
        monthly_pivot["Expense"] = 0

    monthly_pivot["savings"] = monthly_pivot["Income"] - monthly_pivot["Expense"]

    monthly_pivot["savings_rate_percent"] = monthly_pivot.apply(
        lambda row: round((row["savings"] / row["Income"]) * 100, 2)
        if row["Income"] > 0 else 0,
        axis=1
    )

    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    monthly_pivot["month_number"] = monthly_pivot["month"].apply(
        lambda x: month_order.index(x) + 1 if x in month_order else 0
    )

    monthly_pivot = monthly_pivot.sort_values(["year", "month_number"])
    monthly_pivot = monthly_pivot.drop(columns=["month_number"])

    monthly_pivot = monthly_pivot.rename(columns={
        "Income": "monthly_income",
        "Expense": "monthly_expense"
    })

    return monthly_pivot


def calculate_category_summary(df):
    expense_df = df[df["type"] == "Expense"]

    category_summary = expense_df.groupby("category").agg(
        total_spent=("amount", "sum"),
        transaction_count=("amount", "count"),
        average_spent=("amount", "mean"),
        highest_transaction=("amount", "max")
    ).reset_index()

    total_expense = expense_df["amount"].sum()

    category_summary["percentage_of_total_expense"] = category_summary["total_spent"].apply(
        lambda x: round((x / total_expense) * 100, 2) if total_expense > 0 else 0
    )

    category_summary = category_summary.sort_values(
        "total_spent",
        ascending=False
    )

    category_summary["total_spent"] = category_summary["total_spent"].round(2)
    category_summary["average_spent"] = category_summary["average_spent"].round(2)
    category_summary["highest_transaction"] = category_summary["highest_transaction"].round(2)

    return category_summary


def run_transaction_analysis():
    print("=" * 80)
    print("RUNNING TRANSACTION ANALYSIS MODULE")
    print("=" * 80)

    if not CLEANED_FILE.exists():
        print(f"ERROR: File not found: {CLEANED_FILE}")
        print("Run Phase 4 first: clean_personal_finance.py")
        return

    df = pd.read_csv(CLEANED_FILE)

    print(f"Loaded cleaned dataset shape: {df.shape}")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    finance_summary = calculate_finance_summary(df)
    monthly_summary = calculate_monthly_summary(df)
    category_summary = calculate_category_summary(df)

    finance_summary.to_csv(FINANCE_SUMMARY_FILE, index=False)
    monthly_summary.to_csv(MONTHLY_SUMMARY_FILE, index=False)
    category_summary.to_csv(CATEGORY_SUMMARY_FILE, index=False)

    print(f"Finance summary saved to: {FINANCE_SUMMARY_FILE}")
    print(f"Monthly summary saved to: {MONTHLY_SUMMARY_FILE}")
    print(f"Category summary saved to: {CATEGORY_SUMMARY_FILE}")

    print("\nFinance Summary:")
    print(finance_summary)

    print("\nTop Category Summary:")
    print(category_summary.head(10))

    print("\nAnalysis completed successfully.")


if __name__ == "__main__":
    run_transaction_analysis()