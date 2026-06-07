# Personal Finance AI Tracker

A user-ready AI-powered personal finance web application that helps users analyze income, expenses, savings, spending habits, financial health, and budget behavior through an interactive visual dashboard.

The system supports both CSV upload and manual finance planning. Users can upload their transaction data or enter monthly income and expenses manually to receive instant insights, charts, savings analysis, and personalized financial suggestions.

---

## Live Demo

**Dashboard:** Add your deployed Streamlit link here
**Landing Website:** Add GitHub Pages / website link here if deployed

---

## Features

* Upload transaction CSV and analyze financial data
* Manual income and expense entry using Quick Finance Planner
* Automatic transaction cleaning and formatting
* Total income, total expenses, savings, and savings rate calculation
* Category-wise spending analysis
* Monthly income vs expense trend
* Financial health score
* Top spending category detection
* Personalized savings suggestions
* Cleaned CSV download
* Interactive Streamlit dashboard
* Premium frontend landing website using HTML, CSS, and JavaScript

---

## User Modes

### 1. Analyze My Finance

Users can upload a CSV file containing income and expense transactions. The app automatically cleans the file and generates finance insights such as:

* Total income
* Total expenses
* Total savings
* Savings rate
* Top spending category
* Financial health score
* Monthly trend chart
* Category-wise expense chart
* Personalized savings suggestions
* Cleaned CSV download

### 2. Quick Finance Planner

Users who do not have a CSV file can manually enter monthly income and category-wise expenses.

The app then calculates:

* Monthly savings
* Savings rate
* Top spending category
* Financial health status
* Financial health score
* Budget improvement suggestions

---

## CSV Format

The uploaded CSV should contain these required columns:

```text
date, description, amount, type, category
```

Optional columns:

```text
payment_method, merchant, notes
```

Example:

```csv
date,description,amount,type,category,payment_method,merchant,notes
2024-12-01,Salary credited,45000,Income,Salary,Bank Transfer,Company,Monthly salary
2024-12-02,Food order,350,Expense,Food,UPI,Zomato,Dinner
2024-12-03,Bus ticket,80,Expense,Travel,UPI,Bus,Travel
```

---

## Tech Stack

* Python
* Pandas
* NumPy
* Scikit-learn
* Streamlit
* Plotly
* Matplotlib
* Seaborn
* HTML
* CSS
* JavaScript

---

## Project Structure

```text
personal-finance-ai-tracker/
│
├── dashboard/
│   └── app.py
│
├── website/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── src/
│   ├── preprocessing/
│   ├── analysis/
│   ├── anomaly/
│   ├── budget/
│   ├── summary/
│   └── utils/
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── sample/
│   └── templates/
│
├── outputs/
│   ├── reports/
│   └── cleaned_data/
│
├── screenshots/
├── requirements.txt
├── README.md
└── main.py
```

---

## How to Run Locally

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_LINK
cd personal-finance-ai-tracker
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

For Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Streamlit dashboard

```bash
streamlit run dashboard/app.py
```

The dashboard will open at:

```text
http://localhost:8501
```

### 6. Open the landing website

Open this file in your browser:

```text
website/index.html
```

---

## Screenshots

Add screenshots inside the `screenshots/` folder and update this section.

Recommended screenshots:

```text
screenshots/
├── website-home.png
├── website-features.png
├── dashboard-home.png
├── analyze-my-finance.png
├── quick-finance-planner.png
└── how-to-use.png
```

Example markdown after adding screenshots:

```markdown
![Website Home](screenshots/website-home.png)
![Dashboard Home](screenshots/dashboard-home.png)
![Analyze My Finance](screenshots/analyze-my-finance.png)
![Quick Finance Planner](screenshots/quick-finance-planner.png)
```

---

## Future Scope

* User authentication
* Cloud database support
* Bank statement parser
* PDF finance report generation
* Advanced ML-based transaction categorization
* Real-time finance tracking
* Online deployment using Streamlit Community Cloud

---

## Author

Created by **Aswin Krishna**.
