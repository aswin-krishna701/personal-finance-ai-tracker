import pandas as pd
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

# Input files
FINANCE_SUMMARY_FILE = BASE_DIR / "outputs" / "reports" / "finance_summary.csv"
CATEGORY_SUMMARY_FILE = BASE_DIR / "outputs" / "reports" / "category_summary.csv"
ANOMALY_REPORT_FILE = BASE_DIR / "outputs" / "reports" / "anomaly_report.csv"

# Output folder
REPORTS_DIR = BASE_DIR / "outputs" / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = REPORTS_DIR / "spending_personality.csv"


def get_category_spending(category_df, category_name):
    row = category_df[category_df["category"] == category_name]

    if row.empty:
        return 0

    return float(row["total_spent"].iloc[0])


def detect_spending_personality(finance_summary, category_summary, anomaly_count):
    total_income = float(finance_summary["total_income"].iloc[0])
    total_expense = float(finance_summary["total_expense"].iloc[0])
    savings_rate = float(finance_summary["savings_rate_percent"].iloc[0])

    food_spending = get_category_spending(category_summary, "Food")
    entertainment_spending = get_category_spending(category_summary, "Entertainment")
    shopping_spending = get_category_spending(category_summary, "Shopping")
    bills_spending = get_category_spending(category_summary, "Bills")
    travel_spending = get_category_spending(category_summary, "Travel")

    want_spending = shopping_spending + entertainment_spending
    lifestyle_spending = food_spending + entertainment_spending + travel_spending

    if total_expense > 0:
        want_ratio = (want_spending / total_expense) * 100
        bills_ratio = (bills_spending / total_expense) * 100
        lifestyle_ratio = (lifestyle_spending / total_expense) * 100
    else:
        want_ratio = 0
        bills_ratio = 0
        lifestyle_ratio = 0

    # Rule-based personality classification
    if savings_rate >= 30:
        personality = "Smart Saver"
        reason = "Your savings rate is above 30%, which shows strong saving behavior."
        suggestion = "Continue tracking monthly expenses and consider investing extra savings carefully."

    elif anomaly_count >= 50:
        personality = "Risky Spender"
        reason = "A high number of unusual transactions were detected in your spending history."
        suggestion = "Review high-value and unusual transactions regularly to avoid unnecessary financial risk."

    elif shopping_spending > food_spending and shopping_spending > bills_spending:
        personality = "Shopping-Focused Spender"
        reason = "Shopping is one of your strongest spending areas compared to other categories."
        suggestion = "Use a 24-hour waiting rule before buying non-essential items."

    elif lifestyle_ratio >= 40:
        personality = "Lifestyle Spender"
        reason = "A large portion of your expenses goes to food, travel, and entertainment."
        suggestion = "Set fixed monthly limits for lifestyle-related expenses."

    elif bills_ratio >= 30 and want_ratio < 25:
        personality = "Essential Spender"
        reason = "Most of your expenses are focused on essential categories like bills."
        suggestion = "Look for ways to reduce recurring bills and improve monthly savings."

    elif savings_rate < 0:
        personality = "Overspending User"
        reason = "Your total expenses are higher than your total income."
        suggestion = "Reduce non-essential expenses and create a strict monthly budget."

    else:
        personality = "Balanced Spender"
        reason = "Your spending is distributed across multiple categories without one extreme pattern."
        suggestion = "Continue monitoring your budget and try to improve your savings rate."

    return {
        "personality_type": personality,
        "reason": reason,
        "suggestion": suggestion,
        "savings_rate_percent": round(savings_rate, 2),
        "want_spending_ratio_percent": round(want_ratio, 2),
        "bills_spending_ratio_percent": round(bills_ratio, 2),
        "lifestyle_spending_ratio_percent": round(lifestyle_ratio, 2),
        "anomaly_count": anomaly_count,
        "total_income": round(total_income, 2),
        "total_expense": round(total_expense, 2)
    }


def run_spending_personality_analysis():
    print("=" * 80)
    print("RUNNING SPENDING PERSONALITY ANALYSIS")
    print("=" * 80)

    if not FINANCE_SUMMARY_FILE.exists():
        print(f"ERROR: File not found: {FINANCE_SUMMARY_FILE}")
        print("Run Phase 7 first: transaction_analysis.py")
        return

    if not CATEGORY_SUMMARY_FILE.exists():
        print(f"ERROR: File not found: {CATEGORY_SUMMARY_FILE}")
        print("Run Phase 7 first: transaction_analysis.py")
        return

    finance_summary = pd.read_csv(FINANCE_SUMMARY_FILE)
    category_summary = pd.read_csv(CATEGORY_SUMMARY_FILE)

    if ANOMALY_REPORT_FILE.exists():
        anomaly_df = pd.read_csv(ANOMALY_REPORT_FILE)
        anomaly_count = len(anomaly_df)
    else:
        anomaly_count = 0

    result = detect_spending_personality(
        finance_summary,
        category_summary,
        anomaly_count
    )

    output_df = pd.DataFrame([result])
    output_df.to_csv(OUTPUT_FILE, index=False)

    print(f"Spending personality report saved to: {OUTPUT_FILE}")

    print("\nSpending Personality Result:")
    print(output_df)

    print("\nAnalysis completed successfully.")


if __name__ == "__main__":
    run_spending_personality_analysis()