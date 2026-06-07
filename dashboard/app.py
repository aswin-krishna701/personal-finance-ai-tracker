import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import sys

# Project root
BASE_DIR = Path(__file__).resolve().parents[1]

# Add src path
sys.path.append(str(BASE_DIR))

from src.preprocessing.user_upload_cleaner import clean_uploaded_csv

# File paths
TEMPLATE_FILE = BASE_DIR / "data" / "templates" / "user_upload_template.csv"

UPLOAD_OUTPUT_DIR = BASE_DIR / "outputs" / "cleaned_data"
UPLOAD_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

st.set_page_config(
    page_title="Personal Finance AI Tracker",
    page_icon="💰",
    layout="wide"
)


def apply_premium_theme():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

        :root {
            --bg: #0a0e1a;
            --bg-2: #0f1424;
            --surface: #141a2e;
            --surface-2: #1a2138;
            --border: rgba(255,255,255,.08);
            --text: #e7ecf5;
            --muted: #8a93ab;
            --primary: #6366f1;
            --primary-2: #8b5cf6;
            --accent: #10b981;
            --danger: #ef4444;
            --warn: #f59e0b;
            --pink: #ec4899;
            --grad: linear-gradient(135deg,#6366f1 0%,#8b5cf6 50%,#ec4899 100%);
            --grad-soft: linear-gradient(135deg,rgba(99,102,241,.15),rgba(139,92,246,.05));
            --shadow: 0 20px 60px -20px rgba(99,102,241,.35);
            --radius: 16px;
        }

        html, body, [class*="css"] {
            font-family: 'Inter', system-ui, sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at 20% 20%, rgba(99,102,241,.20), transparent 38%),
                radial-gradient(circle at 85% 65%, rgba(236,72,153,.14), transparent 42%),
                radial-gradient(circle at 50% 100%, rgba(16,185,129,.10), transparent 35%),
                linear-gradient(135deg, #0a0e1a 0%, #0f1424 45%, #0a0e1a 100%);
            color: var(--text);
        }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        .block-container {
            padding-top: 2rem;
            padding-bottom: 4rem;
            max-width: 1200px;
        }

        section[data-testid="stSidebar"] {
            background:
                linear-gradient(180deg, rgba(10,14,26,.98), rgba(15,20,36,.96));
            border-right: 1px solid var(--border);
            box-shadow: 18px 0 60px -28px rgba(0,0,0,.8);
        }

        section[data-testid="stSidebar"] * {
            color: var(--text) !important;
        }

        div[role="radiogroup"] label {
            background: rgba(255,255,255,.035);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: .72rem .85rem;
            margin-bottom: .5rem;
            transition: all .25s ease;
        }

        div[role="radiogroup"] label:hover {
            background: rgba(99,102,241,.13);
            border-color: rgba(99,102,241,.35);
            transform: translateX(4px);
        }

        h1, h2, h3 {
            font-family: 'Space Grotesk', sans-serif !important;
            letter-spacing: -0.03em;
            color: var(--text) !important;
        }

        h1 {
            font-size: clamp(2.2rem, 5vw, 3.8rem) !important;
            font-weight: 700 !important;
            background: var(--grad);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: .4rem !important;
        }

        p, span, label {
            color: var(--muted);
        }

        div[data-testid="metric-container"] {
            background:
                linear-gradient(180deg, var(--surface), var(--surface-2));
            border: 1px solid var(--border);
            padding: 1.25rem 1.15rem;
            border-radius: 18px;
            box-shadow: var(--shadow);
            transition: all .25s ease;
            position: relative;
            overflow: hidden;
        }

        div[data-testid="metric-container"]::before {
            content: "";
            position: absolute;
            inset: 0;
            background: var(--grad-soft);
            opacity: .7;
            pointer-events: none;
        }

        div[data-testid="metric-container"]:hover {
            transform: translateY(-5px);
            border-color: rgba(99,102,241,.45);
            box-shadow: 0 25px 55px -20px rgba(139,92,246,.65);
        }

        div[data-testid="metric-container"] label {
            color: var(--muted) !important;
            font-weight: 600 !important;
        }

        div[data-testid="metric-container"] [data-testid="stMetricValue"] {
            color: var(--text) !important;
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 700 !important;
        }

        div[data-testid="stDataFrame"] {
            border-radius: 18px;
            overflow: hidden;
            border: 1px solid var(--border);
            box-shadow: 0 20px 50px -25px rgba(0,0,0,.8);
        }

        div[data-testid="stPlotlyChart"] {
            background: linear-gradient(180deg, var(--surface), var(--surface-2));
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 1rem;
            box-shadow: 0 20px 60px -30px rgba(99,102,241,.45);
        }

        .stButton > button,
        div[data-testid="stDownloadButton"] button {
            border-radius: 10px;
            border: 1px solid rgba(99,102,241,.38);
            background: var(--grad);
            color: #ffffff;
            font-weight: 700;
            padding: .75rem 1.25rem;
            box-shadow: var(--shadow);
            transition: all .25s ease;
        }

        .stButton > button:hover,
        div[data-testid="stDownloadButton"] button:hover {
            transform: translateY(-2px);
            box-shadow: 0 25px 50px -15px rgba(139,92,246,.6);
            border-color: rgba(255,255,255,.28);
        }

        div[data-testid="stAlert"] {
            border-radius: 16px;
            border: 1px solid var(--border);
            background: rgba(20,26,46,.82);
            color: var(--text);
        }

        section[data-testid="stFileUploaderDropzone"] {
            background: linear-gradient(180deg, var(--surface), var(--surface-2));
            border: 1px dashed rgba(99,102,241,.45);
            border-radius: 18px;
            padding: 1.5rem;
        }

        section[data-testid="stFileUploaderDropzone"]:hover {
            border-color: rgba(139,92,246,.75);
            background: rgba(99,102,241,.08);
        }

        .premium-hero {
            padding: 1.6rem 1.5rem 1.35rem;
            margin-bottom: 1.5rem;
            border-radius: 22px;
            background:
                radial-gradient(circle at 20% 20%, rgba(99,102,241,.22), transparent 34%),
                radial-gradient(circle at 90% 10%, rgba(236,72,153,.16), transparent 32%),
                linear-gradient(180deg, var(--surface), var(--surface-2));
            border: 1px solid var(--border);
            box-shadow: 0 30px 80px -35px rgba(0,0,0,.9);
        }

        .premium-badge {
            display: inline-flex;
            padding: .38rem .8rem;
            border-radius: 999px;
            border: 1px solid rgba(99,102,241,.28);
            background: rgba(99,102,241,.12);
            color: #a5b4fc;
            font-weight: 700;
            font-size: .82rem;
            margin-bottom: .85rem;
            letter-spacing: .02em;
        }

        .premium-subtitle {
            max-width: 900px;
            color: var(--muted);
            font-size: 1.05rem;
            line-height: 1.7;
            margin-top: .35rem;
        }

        .glass-section {
            background:
                linear-gradient(180deg, var(--surface), var(--surface-2));
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 1.25rem;
            box-shadow: 0 20px 50px -30px rgba(0,0,0,.8);
            margin: 1rem 0;
        }

        .status-pill {
            display: inline-flex;
            padding: .42rem .8rem;
            border-radius: 999px;
            background: rgba(99,102,241,.12);
            border: 1px solid rgba(99,102,241,.28);
            color: #a5b4fc;
            font-weight: 700;
            font-size: .85rem;
        }

        code {
            background: rgba(255,255,255,.06) !important;
            border-radius: 8px !important;
            color: #a5b4fc !important;
            padding: 3px 8px !important;
        }

        @media (max-width: 768px) {
            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }

            h1 {
                font-size: 2.2rem !important;
            }

            div[data-testid="metric-container"] {
                padding: 1rem;
                border-radius: 16px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def make_chart_dark(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(20,26,46,0.55)",
        font=dict(color="#e7ecf5", family="Inter"),
        title_font=dict(color="#e7ecf5", size=20, family="Space Grotesk"),
        colorway=["#6366f1", "#8b5cf6", "#ec4899", "#10b981", "#f59e0b", "#ef4444"],
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#8a93ab")
        ),
        margin=dict(l=30, r=30, t=70, b=30)
    )

    fig.update_xaxes(
        gridcolor="rgba(255,255,255,0.07)",
        zerolinecolor="rgba(255,255,255,0.08)",
        linecolor="rgba(255,255,255,0.08)"
    )

    fig.update_yaxes(
        gridcolor="rgba(255,255,255,0.07)",
        zerolinecolor="rgba(255,255,255,0.08)",
        linecolor="rgba(255,255,255,0.08)"
    )

    return fig


def premium_page_header(title, subtitle, badge="FinanceAI"):
    st.markdown(
        f"""
        <div class="premium-hero">
            <div class="premium-badge">{badge}</div>
            <h1>{title}</h1>
            <p class="premium-subtitle">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def format_currency(value):
    try:
        return f"₹{float(value):,.2f}"
    except Exception:
        return "₹0.00"


def get_finance_status(savings_rate):
    if savings_rate >= 30:
        return "Excellent", 90
    elif savings_rate >= 20:
        return "Good", 75
    elif savings_rate >= 10:
        return "Average", 60
    elif savings_rate >= 0:
        return "Needs Improvement", 45
    else:
        return "Overspending", 25


def sidebar_navigation():
    st.sidebar.markdown(
        """
        <div style="
            padding: 1rem 0 1.2rem;
            border-bottom: 1px solid rgba(255,255,255,.08);
            margin-bottom: 1rem;
        ">
            <div style="
                display: flex;
                align-items: center;
                gap: 0.7rem;
                font-size: 1.35rem;
                font-weight: 850;
                color: white;
            ">
                <span style="
                    width: 38px;
                    height: 38px;
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    border-radius: 14px;
                    background: linear-gradient(135deg, #6366f1, #8b5cf6, #ec4899);
                    color: #ffffff;
                    box-shadow: 0 0 25px rgba(139,92,246,.35);
                ">₹</span>
                FinanceAI
            </div>
            <p style="color:#8a93ab; margin:0.45rem 0 0; font-size:0.9rem;">
                Personal finance assistant
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    page = st.sidebar.radio(
        "Navigate",
        [
            "Home",
            "Analyze My Finance",
            "Quick Finance Planner",
            "How to Use"
        ]
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        <div class="glass-section">
            <span class="status-pill">User Mode</span>
            <p style="margin-top:0.8rem; color:#8a93ab;">
                Upload your CSV or enter values manually to get instant finance insights.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    return page


def page_home():
    premium_page_header(
        "Personal Finance AI Tracker",
        "Analyze your income, expenses, savings, spending habits, and financial health using your own transaction data.",
        "💰 AI Finance Assistant"
    )

    st.markdown(
        """
        <div class="glass-section">
            <h3>What can you do here?</h3>
            <p>
                This app helps you understand your personal finance behavior.
                You can upload your transaction CSV or manually enter monthly income and expenses.
                The system calculates your savings, spending categories, financial health,
                and gives practical suggestions to improve your budget.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="glass-section">
                <h3>📤 Analyze My Finance</h3>
                <p>
                    Upload your transaction CSV and get instant income, expense,
                    savings, category-wise spending, monthly trend, and suggestions.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="glass-section">
                <h3>⚡ Quick Finance Planner</h3>
                <p>
                    Do not have a CSV? Enter your monthly income and expenses manually
                    to get instant savings analysis and budget advice.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.subheader("Why this is useful")

    col3, col4, col5 = st.columns(3)

    col3.metric("Understand Spending", "Category-wise")
    col4.metric("Track Savings", "Monthly")
    col5.metric("Improve Budget", "AI Suggestions")

    st.markdown(
        """
        <div class="glass-section">
            <h3>Start Here</h3>
            <p>
                Use <b>Analyze My Finance</b> if you have a CSV file.
                Use <b>Quick Finance Planner</b> if you want to type your monthly income and expenses manually.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


def analyze_uploaded_transactions(cleaned_df):
    expense_df = cleaned_df[cleaned_df["type"] == "Expense"].copy()
    income_df = cleaned_df[cleaned_df["type"] == "Income"].copy()

    total_income = income_df["amount"].sum()
    total_expense = expense_df["amount"].sum()
    total_savings = total_income - total_expense

    savings_rate = (total_savings / total_income) * 100 if total_income > 0 else 0

    top_category = "None"
    if not expense_df.empty:
        top_category = expense_df.groupby("category")["amount"].sum().idxmax()

    category_summary = pd.DataFrame()

    if not expense_df.empty:
        category_summary = expense_df.groupby("category").agg(
            total_spent=("amount", "sum"),
            transaction_count=("amount", "count"),
            average_spent=("amount", "mean")
        ).reset_index()

        total_exp = expense_df["amount"].sum()

        category_summary["percentage"] = category_summary["total_spent"].apply(
            lambda x: round((x / total_exp) * 100, 2) if total_exp > 0 else 0
        )

        category_summary["total_spent"] = category_summary["total_spent"].round(2)
        category_summary["average_spent"] = category_summary["average_spent"].round(2)
        category_summary = category_summary.sort_values("total_spent", ascending=False)

    monthly_summary = pd.DataFrame()

    if not cleaned_df.empty:
        monthly_summary = cleaned_df.groupby(["year", "month", "type"])["amount"].sum().reset_index()

        monthly_summary = monthly_summary.pivot_table(
            index=["year", "month"],
            columns="type",
            values="amount",
            fill_value=0
        ).reset_index()

        if "Income" not in monthly_summary.columns:
            monthly_summary["Income"] = 0

        if "Expense" not in monthly_summary.columns:
            monthly_summary["Expense"] = 0

        monthly_summary["savings"] = monthly_summary["Income"] - monthly_summary["Expense"]

        month_order = {
            "January": 1,
            "February": 2,
            "March": 3,
            "April": 4,
            "May": 5,
            "June": 6,
            "July": 7,
            "August": 8,
            "September": 9,
            "October": 10,
            "November": 11,
            "December": 12
        }

        monthly_summary["month_number"] = monthly_summary["month"].map(month_order)
        monthly_summary["period"] = (
            monthly_summary["year"].astype(str)
            + "-"
            + monthly_summary["month_number"].astype(str).str.zfill(2)
        )

        monthly_summary = monthly_summary.sort_values(["year", "month_number"])

    health_status, health_score = get_finance_status(savings_rate)

    suggestions = []

    if total_income == 0:
        suggestions.append("No income transaction found. Add income entries to calculate savings properly.")

    if total_expense > total_income:
        suggestions.append("Your expenses are higher than your income. Reduce non-essential spending first.")

    if savings_rate < 20 and total_income > 0:
        suggestions.append("Your savings rate is below 20%. Try to save at least 20% of your income.")

    if top_category != "None":
        suggestions.append(f"Your highest spending category is {top_category}. Track this category carefully.")

    if not category_summary.empty:
        for _, row in category_summary.head(3).iterrows():
            category = row["category"]
            percentage = row["percentage"]

            if category == "Food" and percentage >= 15:
                suggestions.append("Food spending is high. Set a weekly food budget and reduce outside food orders.")

            elif category == "Shopping" and percentage >= 10:
                suggestions.append("Shopping spending is high. Use a 24-hour waiting rule before non-essential purchases.")

            elif category == "Travel" and percentage >= 10:
                suggestions.append("Travel spending is high. Plan routes and compare cheaper transport options.")

            elif category == "Subscriptions" and percentage >= 5:
                suggestions.append("Subscriptions are noticeable. Cancel unused monthly subscriptions.")

            elif category == "Entertainment" and percentage >= 10:
                suggestions.append("Entertainment spending is high. Set a fixed entertainment budget.")

    if not suggestions:
        suggestions.append("Your spending pattern looks controlled. Continue tracking expenses regularly.")

    summary_text = (
        f"Your uploaded data shows total income of {format_currency(total_income)} and total expenses of "
        f"{format_currency(total_expense)}. Your savings are {format_currency(total_savings)}, with a savings rate of "
        f"{savings_rate:.2f}%. The highest spending category is {top_category}. "
        f"Financial status: {health_status}. Main suggestion: {suggestions[0]}"
    )

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "total_savings": total_savings,
        "savings_rate": savings_rate,
        "top_category": top_category,
        "category_summary": category_summary,
        "monthly_summary": monthly_summary,
        "suggestions": suggestions,
        "health_status": health_status,
        "health_score": health_score,
        "summary_text": summary_text
    }


def page_analyze_my_finance():
    premium_page_header(
        "Analyze My Finance",
        "Upload your own transaction CSV to get instant savings, spending, category, and financial health insights.",
        "📤 CSV Finance Analyzer"
    )

    st.markdown(
        """
        <div class="glass-section">
            <h3>Required CSV Columns</h3>
            <p><code>date, description, amount, type, category</code></p>
            <h3>Optional Columns</h3>
            <p><code>payment_method, merchant, notes</code></p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if TEMPLATE_FILE.exists():
        with open(TEMPLATE_FILE, "rb") as file:
            st.download_button(
                label="Download CSV Template",
                data=file,
                file_name="user_upload_template.csv",
                mime="text/csv"
            )

    uploaded_file = st.file_uploader("Upload your transaction CSV file", type=["csv"])

    if uploaded_file is not None:
        temp_upload_file = UPLOAD_OUTPUT_DIR / "temp_user_upload.csv"

        with open(temp_upload_file, "wb") as file:
            file.write(uploaded_file.getbuffer())

        cleaned_output_file = UPLOAD_OUTPUT_DIR / "uploaded_transactions_cleaned.csv"

        cleaned_df = clean_uploaded_csv(
            input_file=temp_upload_file,
            output_file=cleaned_output_file
        )

        if cleaned_df is not None:
            st.success("CSV uploaded, cleaned, and analyzed successfully.")

            analysis = analyze_uploaded_transactions(cleaned_df)

            st.subheader("Your Finance Summary")

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Income", format_currency(analysis["total_income"]))
            col2.metric("Total Expenses", format_currency(analysis["total_expense"]))
            col3.metric("Total Savings", format_currency(analysis["total_savings"]))
            col4.metric("Savings Rate", f"{analysis['savings_rate']:.2f}%")

            col5, col6, col7 = st.columns(3)
            col5.metric("Top Spending Category", analysis["top_category"])
            col6.metric("Financial Status", analysis["health_status"])
            col7.metric("Health Score", f"{analysis['health_score']}/100")

            st.subheader("AI Finance Summary")
            st.success(analysis["summary_text"])

            category_summary = analysis["category_summary"]

            if not category_summary.empty:
                st.subheader("Category-wise Spending Analysis")

                chart_col1, chart_col2 = st.columns(2)

                with chart_col1:
                    fig_pie = px.pie(
                        category_summary,
                        names="category",
                        values="total_spent",
                        title="Category Split",
                        hole=0.45
                    )
                    st.plotly_chart(make_chart_dark(fig_pie), use_container_width=True)

                with chart_col2:
                    fig_bar = px.bar(
                        category_summary,
                        x="category",
                        y="total_spent",
                        title="Spending by Category",
                        text="total_spent"
                    )
                    st.plotly_chart(make_chart_dark(fig_bar), use_container_width=True)

                st.dataframe(category_summary, use_container_width=True)

            monthly_summary = analysis["monthly_summary"]

            if not monthly_summary.empty:
                st.subheader("Monthly Income, Expense, and Savings Trend")

                fig_monthly = px.line(
                    monthly_summary,
                    x="period",
                    y=["Income", "Expense", "savings"],
                    title="Monthly Trend",
                    markers=True
                )
                st.plotly_chart(make_chart_dark(fig_monthly), use_container_width=True)

                st.dataframe(monthly_summary, use_container_width=True)

            st.subheader("Personalized Savings Suggestions")

            for suggestion in analysis["suggestions"]:
                st.warning(suggestion)

            st.subheader("Cleaned Uploaded Transactions")
            st.dataframe(cleaned_df, use_container_width=True)

            with open(cleaned_output_file, "rb") as file:
                st.download_button(
                    label="Download Cleaned CSV",
                    data=file,
                    file_name="uploaded_transactions_cleaned.csv",
                    mime="text/csv"
                )


def page_quick_finance_planner():
    premium_page_header(
        "Quick Finance Planner",
        "Enter your monthly income and expenses manually to get instant savings analysis, budget advice, and financial health status.",
        "⚡ Manual Finance Analyzer"
    )

    st.markdown(
        """
        <div class="glass-section">
            <h3>Manual Monthly Finance Input</h3>
            <p>
                Use this when you do not have a CSV file. Enter monthly income and category-wise expenses,
                and the app will calculate savings, spending pattern, health status, and suggestions.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("Income and Savings Goal")

    col1, col2 = st.columns(2)

    with col1:
        monthly_income = st.number_input(
            "Monthly Income",
            min_value=0.0,
            value=45000.0,
            step=500.0
        )

    with col2:
        savings_goal_percent = st.slider(
            "Target Savings Rate (%)",
            min_value=0,
            max_value=60,
            value=20,
            step=5
        )

    st.subheader("Monthly Expenses by Category")

    col1, col2, col3 = st.columns(3)

    with col1:
        food = st.number_input("Food", min_value=0.0, value=6000.0, step=500.0)
        travel = st.number_input("Travel", min_value=0.0, value=3000.0, step=500.0)
        shopping = st.number_input("Shopping", min_value=0.0, value=4000.0, step=500.0)

    with col2:
        bills = st.number_input("Bills / Rent / Utilities", min_value=0.0, value=9000.0, step=500.0)
        entertainment = st.number_input("Entertainment", min_value=0.0, value=2500.0, step=500.0)
        subscriptions = st.number_input("Subscriptions", min_value=0.0, value=1000.0, step=250.0)

    with col3:
        health = st.number_input("Health", min_value=0.0, value=2000.0, step=500.0)
        education = st.number_input("Education", min_value=0.0, value=3000.0, step=500.0)
        others = st.number_input("Others", min_value=0.0, value=2500.0, step=500.0)

    expense_data = {
        "Food": food,
        "Travel": travel,
        "Shopping": shopping,
        "Bills": bills,
        "Entertainment": entertainment,
        "Subscriptions": subscriptions,
        "Health": health,
        "Education": education,
        "Others": others
    }

    total_expense = sum(expense_data.values())
    monthly_savings = monthly_income - total_expense
    savings_rate = (monthly_savings / monthly_income) * 100 if monthly_income > 0 else 0

    required_savings = monthly_income * (savings_goal_percent / 100)
    extra_savings_needed = required_savings - monthly_savings

    top_category = max(expense_data, key=expense_data.get)
    health_status, health_score = get_finance_status(savings_rate)

    st.subheader("Instant Finance Summary")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Monthly Income", format_currency(monthly_income))
    col2.metric("Total Expenses", format_currency(total_expense))
    col3.metric("Monthly Savings", format_currency(monthly_savings))
    col4.metric("Savings Rate", f"{savings_rate:.2f}%")

    col5, col6, col7 = st.columns(3)
    col5.metric("Top Spending Category", top_category)
    col6.metric("Financial Health", health_status)
    col7.metric("Health Score", f"{health_score}/100")

    category_df = pd.DataFrame({
        "category": list(expense_data.keys()),
        "amount": list(expense_data.values())
    })

    category_df = category_df[category_df["amount"] > 0].sort_values("amount", ascending=False)

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        fig_pie = px.pie(
            category_df,
            names="category",
            values="amount",
            title="Expense Category Split",
            hole=0.45
        )
        st.plotly_chart(make_chart_dark(fig_pie), use_container_width=True)

    with chart_col2:
        fig_bar = px.bar(
            category_df,
            x="category",
            y="amount",
            title="Expense by Category",
            text="amount"
        )
        st.plotly_chart(make_chart_dark(fig_bar), use_container_width=True)

    st.subheader("AI Finance Summary")

    if monthly_income == 0:
        summary_text = "Please enter monthly income to calculate savings rate and financial health properly."
    else:
        summary_text = (
            f"Your monthly income is {format_currency(monthly_income)} and your total monthly expenses are "
            f"{format_currency(total_expense)}. Your monthly savings are {format_currency(monthly_savings)}, "
            f"with a savings rate of {savings_rate:.2f}%. Your highest spending category is {top_category}. "
            f"Your financial health status is {health_status}."
        )

    st.success(summary_text)

    st.subheader("Personalized Suggestions")

    suggestions = []

    if total_expense > monthly_income:
        suggestions.append("Your expenses are higher than your income. Reduce non-essential expenses immediately.")

    if savings_rate < savings_goal_percent:
        suggestions.append(
            f"Your savings rate is below your target of {savings_goal_percent}%. "
            f"Try to save at least {format_currency(required_savings)} per month."
        )

    if extra_savings_needed > 0:
        suggestions.append(
            f"You need to reduce expenses or increase income by around {format_currency(extra_savings_needed)} "
            f"to reach your savings goal."
        )

    if monthly_income > 0:
        if food > monthly_income * 0.15:
            suggestions.append("Food spending is high. Set a weekly food budget and reduce outside food orders.")

        if shopping > monthly_income * 0.10:
            suggestions.append("Shopping spending is high. Use a 24-hour waiting rule before buying non-essential items.")

        if entertainment > monthly_income * 0.08:
            suggestions.append("Entertainment spending is high. Set a fixed monthly entertainment limit.")

        if subscriptions > monthly_income * 0.05:
            suggestions.append("Subscriptions are taking a noticeable part of income. Cancel unused subscriptions.")

        if bills > monthly_income * 0.35:
            suggestions.append("Bills and rent are high compared to income. Review fixed costs where possible.")

    if not suggestions:
        suggestions.append("Your spending looks controlled. Continue tracking your expenses every month.")

    for suggestion in suggestions:
        st.warning(suggestion)

    st.subheader("Manual Expense Table")
    st.dataframe(category_df, use_container_width=True)


def page_how_to_use():
    premium_page_header(
        "How to Use",
        "Follow these simple steps to analyze your personal finance data.",
        "📘 User Guide"
    )

    st.markdown(
        """
        <div class="glass-section">
            <h3>Option 1: Upload CSV</h3>
            <p>Use this option if you have transaction data in CSV format.</p>

            <h4>Required CSV Columns</h4>
            <p><code>date, description, amount, type, category</code></p>

            <h4>Optional Columns</h4>
            <p><code>payment_method, merchant, notes</code></p>

            <h4>Example Rows</h4>
            <p><code>2024-12-01, Salary credited, 45000, Income, Salary</code></p>
            <p><code>2024-12-02, Zomato order, 350, Expense, Food</code></p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="glass-section">
            <h3>Option 2: Manual Entry</h3>
            <p>
                Use Quick Finance Planner if you do not have a CSV file.
                Enter your monthly income and expenses manually.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="glass-section">
            <h3>What the app gives you</h3>
            <p>After upload or manual entry, the app shows:</p>
            <ul>
                <li>Total income</li>
                <li>Total expenses</li>
                <li>Monthly savings</li>
                <li>Savings rate</li>
                <li>Top spending category</li>
                <li>Financial health status</li>
                <li>Category-wise charts</li>
                <li>Monthly trend chart for CSV uploads</li>
                <li>Personalized savings suggestions</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    if TEMPLATE_FILE.exists():
        with open(TEMPLATE_FILE, "rb") as file:
            st.download_button(
                label="Download CSV Template",
                data=file,
                file_name="user_upload_template.csv",
                mime="text/csv"
            )


def main():
    page = sidebar_navigation()

    if page == "Home":
        page_home()
    elif page == "Analyze My Finance":
        page_analyze_my_finance()
    elif page == "Quick Finance Planner":
        page_quick_finance_planner()
    elif page == "How to Use":
        page_how_to_use()


if __name__ == "__main__":
    apply_premium_theme()
    main()