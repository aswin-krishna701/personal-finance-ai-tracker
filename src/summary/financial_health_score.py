import pandas as pd
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

# Input files
FINANCE_SUMMARY_FILE = BASE_DIR / "outputs" / "reports" / "finance_summary.csv"
BUDGET_REPORT_FILE = BASE_DIR / "outputs" / "reports" / "budget_report.csv"
ANOMALY_REPORT_FILE = BASE_DIR / "outputs" / "reports" / "anomaly_report.csv"
MONTHLY_SUMMARY_FILE = BASE_DIR / "outputs" / "reports" / "monthly_summary.csv"

# Output file
REPORTS_DIR = BASE_DIR / "outputs" / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = REPORTS_DIR / "financial_health_score.csv"


def get_score_status(score):
    if score >= 85:
        return "Excellent"
    elif score >= 70:
        return "Good"
    elif score >= 50:
        return "Average"
    else:
        return "Needs Improvement"


def calculate_savings_score(savings_rate):
    """
    Max 40 marks.
    """
    if savings_rate >= 30:
        return 40
    elif savings_rate >= 20:
        return 30
    elif savings_rate >= 10:
        return 20
    elif savings_rate >= 0:
        return 10
    else:
        return 0


def calculate_budget_score():
    """
    Max 25 marks.
    Based on number of over-budget categories.
    """
    if not BUDGET_REPORT_FILE.exists():
        return 15

    budget_df = pd.read_csv(BUDGET_REPORT_FILE)

    total_categories = len(budget_df)
    over_budget_count = len(budget_df[budget_df["alert_status"] == "Over Budget"])

    if total_categories == 0:
        return 15

    over_budget_ratio = over_budget_count / total_categories

    if over_budget_ratio == 0:
        return 25
    elif over_budget_ratio <= 0.25:
        return 20
    elif over_budget_ratio <= 0.50:
        return 15
    elif over_budget_ratio <= 0.75:
        return 8
    else:
        return 3


def calculate_expense_stability_score():
    """
    Max 20 marks.
    Based on monthly expense variation.
    """
    if not MONTHLY_SUMMARY_FILE.exists():
        return 10

    monthly_df = pd.read_csv(MONTHLY_SUMMARY_FILE)

    if "monthly_expense" not in monthly_df.columns:
        return 10

    avg_expense = monthly_df["monthly_expense"].mean()
    std_expense = monthly_df["monthly_expense"].std()

    if avg_expense == 0 or pd.isna(std_expense):
        return 10

    variation_ratio = std_expense / avg_expense

    if variation_ratio <= 0.20:
        return 20
    elif variation_ratio <= 0.40:
        return 15
    elif variation_ratio <= 0.60:
        return 10
    else:
        return 5


def calculate_anomaly_score():
    """
    Max 15 marks.
    Lower anomaly count gives better score.
    """
    if not ANOMALY_REPORT_FILE.exists():
        return 10

    anomaly_df = pd.read_csv(ANOMALY_REPORT_FILE)
    anomaly_count = len(anomaly_df)

    if anomaly_count == 0:
        return 15
    elif anomaly_count <= 20:
        return 12
    elif anomaly_count <= 50:
        return 8
    elif anomaly_count <= 100:
        return 5
    else:
        return 2


def run_financial_health_score():
    print("=" * 80)
    print("RUNNING FINANCIAL HEALTH SCORE MODULE")
    print("=" * 80)

    if not FINANCE_SUMMARY_FILE.exists():
        print(f"ERROR: File not found: {FINANCE_SUMMARY_FILE}")
        print("Run Phase 7 first: transaction_analysis.py")
        return

    finance_summary = pd.read_csv(FINANCE_SUMMARY_FILE)

    savings_rate = float(finance_summary["savings_rate_percent"].iloc[0])

    savings_score = calculate_savings_score(savings_rate)
    budget_score = calculate_budget_score()
    stability_score = calculate_expense_stability_score()
    anomaly_score = calculate_anomaly_score()

    total_score = savings_score + budget_score + stability_score + anomaly_score
    status = get_score_status(total_score)

    result = {
        "financial_health_score": total_score,
        "status": status,
        "savings_score_out_of_40": savings_score,
        "budget_score_out_of_25": budget_score,
        "expense_stability_score_out_of_20": stability_score,
        "anomaly_score_out_of_15": anomaly_score,
        "savings_rate_percent": round(savings_rate, 2)
    }

    output_df = pd.DataFrame([result])
    output_df.to_csv(OUTPUT_FILE, index=False)

    print(f"Financial health score saved to: {OUTPUT_FILE}")

    print("\nFinancial Health Score:")
    print(output_df)

    print("\nFinancial health score calculation completed successfully.")


if __name__ == "__main__":
    run_financial_health_score()