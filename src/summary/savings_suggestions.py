import pandas as pd
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

# Input files
FINANCE_SUMMARY_FILE = BASE_DIR / "outputs" / "reports" / "finance_summary.csv"
CATEGORY_SUMMARY_FILE = BASE_DIR / "outputs" / "reports" / "category_summary.csv"
BUDGET_REPORT_FILE = BASE_DIR / "outputs" / "reports" / "budget_report.csv"
PERSONALITY_FILE = BASE_DIR / "outputs" / "reports" / "spending_personality.csv"

# Output folder
REPORTS_DIR = BASE_DIR / "outputs" / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = REPORTS_DIR / "savings_suggestions.csv"


def add_suggestion(suggestions, priority, area, problem, suggestion):
    suggestions.append({
        "priority": priority,
        "area": area,
        "problem": problem,
        "suggestion": suggestion
    })


def run_savings_suggestions():
    print("=" * 80)
    print("RUNNING SAVINGS SUGGESTIONS MODULE")
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

    suggestions = []

    total_income = float(finance_summary["total_income"].iloc[0])
    total_expense = float(finance_summary["total_expense"].iloc[0])
    savings_rate = float(finance_summary["savings_rate_percent"].iloc[0])
    top_category = str(finance_summary["top_spending_category"].iloc[0])

    # General savings condition
    if total_expense > total_income:
        add_suggestion(
            suggestions,
            "High",
            "Overall Spending",
            "Your total expenses are higher than your total income.",
            "Reduce non-essential expenses first and create a strict monthly budget plan."
        )

    if savings_rate < 20:
        add_suggestion(
            suggestions,
            "High",
            "Savings Rate",
            f"Your savings rate is low at {round(savings_rate, 2)}%.",
            "Try to save at least 20% of your income by limiting wants and tracking daily expenses."
        )

    # Category-based suggestions
    for _, row in category_summary.iterrows():
        category = row["category"]
        total_spent = float(row["total_spent"])
        percentage = float(row["percentage_of_total_expense"])

        if category == "Food" and percentage >= 12:
            add_suggestion(
                suggestions,
                "Medium",
                "Food",
                f"Food spending is {percentage}% of total expenses.",
                "Reduce outside food orders and set a weekly food budget."
            )

        elif category == "Shopping" and percentage >= 10:
            add_suggestion(
                suggestions,
                "Medium",
                "Shopping",
                f"Shopping spending is {percentage}% of total expenses.",
                "Use a 24-hour waiting rule before buying non-essential items."
            )

        elif category == "Entertainment" and percentage >= 10:
            add_suggestion(
                suggestions,
                "Medium",
                "Entertainment",
                f"Entertainment spending is {percentage}% of total expenses.",
                "Set a fixed monthly entertainment limit and avoid impulse spending."
            )

        elif category == "Travel" and percentage >= 10:
            add_suggestion(
                suggestions,
                "Medium",
                "Travel",
                f"Travel spending is {percentage}% of total expenses.",
                "Plan travel expenses in advance and compare cheaper transport options."
            )

        elif category == "Bills" and percentage >= 20:
            add_suggestion(
                suggestions,
                "Medium",
                "Bills",
                f"Bills are the highest spending area at {percentage}% of total expenses.",
                "Review electricity, internet, rent, and other recurring bills to reduce fixed costs."
            )

    # Budget-based suggestions
    if BUDGET_REPORT_FILE.exists():
        budget_report = pd.read_csv(BUDGET_REPORT_FILE)

        over_budget = budget_report[budget_report["alert_status"] == "Over Budget"]

        for _, row in over_budget.head(5).iterrows():
            add_suggestion(
                suggestions,
                "High",
                f"Budget - {row['category']}",
                f"{row['category']} crossed the planned budget.",
                f"Reduce spending in {row['category']} and set a realistic monthly limit."
            )

    # Personality-based suggestion
    if PERSONALITY_FILE.exists():
        personality_df = pd.read_csv(PERSONALITY_FILE)
        personality = str(personality_df["personality_type"].iloc[0])

        if personality == "Risky Spender":
            add_suggestion(
                suggestions,
                "High",
                "Spending Personality",
                "Your spending personality is Risky Spender.",
                "Review unusual and high-value transactions regularly before making new purchases."
            )

        elif personality == "Smart Saver":
            add_suggestion(
                suggestions,
                "Low",
                "Spending Personality",
                "Your spending personality is Smart Saver.",
                "Continue your saving habit and consider planning long-term financial goals."
            )

    # Top category suggestion
    add_suggestion(
        suggestions,
        "Medium",
        "Top Category",
        f"Your highest spending category is {top_category}.",
        f"Track {top_category} expenses carefully because it has the largest impact on your budget."
    )

    suggestions_df = pd.DataFrame(suggestions)

    # Remove duplicate suggestions
    suggestions_df = suggestions_df.drop_duplicates()

    # Save output
    suggestions_df.to_csv(OUTPUT_FILE, index=False)

    print(f"Savings suggestions saved to: {OUTPUT_FILE}")

    print("\nSavings Suggestions:")
    print(suggestions_df)

    print("\nSavings suggestions completed successfully.")


if __name__ == "__main__":
    run_savings_suggestions()