import pandas as pd
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

# Input files
MONTHLY_SUMMARY_FILE = BASE_DIR / "outputs" / "reports" / "monthly_summary.csv"
CATEGORY_SUMMARY_FILE = BASE_DIR / "outputs" / "reports" / "category_summary.csv"
BUDGET_REPORT_FILE = BASE_DIR / "outputs" / "reports" / "budget_report.csv"
ANOMALY_REPORT_FILE = BASE_DIR / "outputs" / "reports" / "anomaly_report.csv"
PERSONALITY_FILE = BASE_DIR / "outputs" / "reports" / "spending_personality.csv"
SUGGESTIONS_FILE = BASE_DIR / "outputs" / "reports" / "savings_suggestions.csv"

# Output files
REPORTS_DIR = BASE_DIR / "outputs" / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

SUMMARY_TXT_FILE = REPORTS_DIR / "monthly_ai_summary.txt"
SUMMARY_CSV_FILE = REPORTS_DIR / "monthly_ai_summary.csv"


def get_financial_status(savings_rate):
    if savings_rate >= 30:
        return "Excellent"
    elif savings_rate >= 20:
        return "Good"
    elif savings_rate >= 10:
        return "Average"
    elif savings_rate >= 0:
        return "Needs Improvement"
    else:
        return "Overspending"


def run_monthly_ai_summary():
    print("=" * 80)
    print("RUNNING MONTHLY AI FINANCE SUMMARY")
    print("=" * 80)

    if not MONTHLY_SUMMARY_FILE.exists():
        print(f"ERROR: File not found: {MONTHLY_SUMMARY_FILE}")
        print("Run Phase 7 first: transaction_analysis.py")
        return

    if not CATEGORY_SUMMARY_FILE.exists():
        print(f"ERROR: File not found: {CATEGORY_SUMMARY_FILE}")
        print("Run Phase 7 first: transaction_analysis.py")
        return

    monthly_df = pd.read_csv(MONTHLY_SUMMARY_FILE)
    category_df = pd.read_csv(CATEGORY_SUMMARY_FILE)

    # Select latest month available in dataset
    latest_row = monthly_df.tail(1).iloc[0]

    year = latest_row["year"]
    month = latest_row["month"]
    monthly_income = float(latest_row["monthly_income"])
    monthly_expense = float(latest_row["monthly_expense"])
    monthly_savings = float(latest_row["savings"])
    savings_rate = float(latest_row["savings_rate_percent"])

    status = get_financial_status(savings_rate)

    # Top categories
    top_categories = category_df.head(3)["category"].tolist()
    top_categories_text = ", ".join(top_categories)

    # Budget alerts
    over_budget_categories = []

    if BUDGET_REPORT_FILE.exists():
        budget_df = pd.read_csv(BUDGET_REPORT_FILE)
        over_budget_categories = budget_df[
            budget_df["alert_status"] == "Over Budget"
        ]["category"].head(3).tolist()

    if over_budget_categories:
        budget_text = "You crossed the budget limit in " + ", ".join(over_budget_categories) + "."
    else:
        budget_text = "No major budget limit was crossed."

    # Anomaly count
    if ANOMALY_REPORT_FILE.exists():
        anomaly_df = pd.read_csv(ANOMALY_REPORT_FILE)
        anomaly_count = len(anomaly_df)
    else:
        anomaly_count = 0

    # Personality
    if PERSONALITY_FILE.exists():
        personality_df = pd.read_csv(PERSONALITY_FILE)
        personality = personality_df["personality_type"].iloc[0]
    else:
        personality = "Not Available"

    # Top suggestion
    if SUGGESTIONS_FILE.exists():
        suggestions_df = pd.read_csv(SUGGESTIONS_FILE)
        top_suggestion = suggestions_df["suggestion"].iloc[0]
    else:
        top_suggestion = "Track your expenses regularly and maintain a monthly budget."

    summary_text = (
        f"In {month} {year}, your total income was ₹{monthly_income:,.2f} "
        f"and your total expenses were ₹{monthly_expense:,.2f}. "
        f"Your savings were ₹{monthly_savings:,.2f}, with a savings rate of "
        f"{savings_rate:.2f}%. "
        f"The highest spending categories were {top_categories_text}. "
        f"{budget_text} "
        f"A total of {anomaly_count} unusual transactions were detected in the available data. "
        f"Your spending personality is classified as {personality}. "
        f"Overall, your financial health for this period is {status}. "
        f"Main suggestion: {top_suggestion}"
    )

    output_df = pd.DataFrame([{
        "month": month,
        "year": year,
        "monthly_income": round(monthly_income, 2),
        "monthly_expense": round(monthly_expense, 2),
        "monthly_savings": round(monthly_savings, 2),
        "savings_rate_percent": round(savings_rate, 2),
        "top_categories": top_categories_text,
        "over_budget_categories": ", ".join(over_budget_categories),
        "anomaly_count": anomaly_count,
        "spending_personality": personality,
        "financial_status": status,
        "summary": summary_text
    }])

    # Save TXT summary
    with open(SUMMARY_TXT_FILE, "w", encoding="utf-8") as file:
        file.write(summary_text)

    # Save CSV summary
    output_df.to_csv(SUMMARY_CSV_FILE, index=False)

    print(f"Monthly AI summary TXT saved to: {SUMMARY_TXT_FILE}")
    print(f"Monthly AI summary CSV saved to: {SUMMARY_CSV_FILE}")

    print("\nMonthly AI Finance Summary:")
    print(summary_text)

    print("\nMonthly AI summary completed successfully.")


if __name__ == "__main__":
    run_monthly_ai_summary()