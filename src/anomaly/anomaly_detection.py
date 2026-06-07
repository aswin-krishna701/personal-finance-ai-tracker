import pandas as pd
from pathlib import Path
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder

# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

# Input files
PERSONAL_FILE = BASE_DIR / "data" / "processed" / "personal_finance_cleaned.csv"
CARD_FILE = BASE_DIR / "data" / "processed" / "card_transactions_cleaned.csv"

# Output folder
REPORTS_DIR = BASE_DIR / "outputs" / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

ANOMALY_REPORT_FILE = REPORTS_DIR / "anomaly_report.csv"


def prepare_personal_finance_data():
    df = pd.read_csv(PERSONAL_FILE)

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date", "amount"])

    # Use only expenses for anomaly detection
    df = df[df["type"] == "Expense"].copy()

    df["source_dataset"] = "Personal Finance"
    df["merchant"] = df["merchant"].fillna("Unknown")
    df["is_fraud"] = "Not Available"

    return df


def prepare_card_data():
    df = pd.read_csv(CARD_FILE)

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date", "amount"])

    df["source_dataset"] = "Credit Card"

    return df


def encode_column(df, column_name):
    encoder = LabelEncoder()
    df[column_name] = df[column_name].astype(str)
    return encoder.fit_transform(df[column_name])


def create_anomaly_reason(row):
    reasons = []

    if row["amount"] >= row["amount_95_percentile"]:
        reasons.append("High-value transaction")

    if row["category_count"] <= 3:
        reasons.append("Rare category spending")

    if row["same_day_transaction_count"] >= 5:
        reasons.append("Frequent spending on same day")

    if row["isolation_forest_result"] == -1:
        reasons.append("ML anomaly detected")

    if not reasons:
        reasons.append("Unusual transaction pattern")

    return ", ".join(reasons)


def run_anomaly_detection():
    print("=" * 80)
    print("RUNNING ANOMALY DETECTION MODULE")
    print("=" * 80)

    if not PERSONAL_FILE.exists():
        print(f"ERROR: File not found: {PERSONAL_FILE}")
        return

    if not CARD_FILE.exists():
        print(f"ERROR: File not found: {CARD_FILE}")
        return

    personal_df = prepare_personal_finance_data()
    card_df = prepare_card_data()

    print(f"Personal finance expense rows: {personal_df.shape}")
    print(f"Credit card rows: {card_df.shape}")

    # Keep common useful columns
    personal_df = personal_df[[
        "date",
        "type",
        "category",
        "description",
        "amount",
        "merchant",
        "month",
        "year",
        "day_name",
        "is_fraud",
        "source_dataset"
    ]]

    card_df = card_df[[
        "date",
        "type",
        "category",
        "description",
        "amount",
        "merchant",
        "month",
        "year",
        "day_name",
        "is_fraud",
        "source_dataset"
    ]]

    # Combine both datasets
    df = pd.concat([personal_df, card_df], ignore_index=True)

    # Feature engineering
    df["day_of_week"] = pd.to_datetime(df["date"]).dt.dayofweek
    df["category_encoded"] = encode_column(df, "category")
    df["merchant_encoded"] = encode_column(df, "merchant")

    df["category_count"] = df.groupby("category")["category"].transform("count")
    df["same_day_transaction_count"] = df.groupby("date")["date"].transform("count")
    df["amount_95_percentile"] = df["amount"].quantile(0.95)

    features = [
        "amount",
        "day_of_week",
        "category_encoded",
        "merchant_encoded"
    ]

    model = IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42
    )

    df["isolation_forest_result"] = model.fit_predict(df[features])

    # Keep only anomalies
    anomalies = df[df["isolation_forest_result"] == -1].copy()

    anomalies["anomaly_reason"] = anomalies.apply(create_anomaly_reason, axis=1)

    final_columns = [
        "date",
        "source_dataset",
        "type",
        "category",
        "description",
        "amount",
        "merchant",
        "is_fraud",
        "anomaly_reason",
        "month",
        "year",
        "day_name"
    ]

    anomalies = anomalies[final_columns]

    anomalies = anomalies.sort_values("amount", ascending=False)

    anomalies.to_csv(ANOMALY_REPORT_FILE, index=False)

    print(f"Total combined rows: {df.shape[0]}")
    print(f"Detected anomalies: {anomalies.shape[0]}")
    print(f"Anomaly report saved to: {ANOMALY_REPORT_FILE}")

    print("\nTop 10 Anomalies:")
    print(anomalies.head(10))

    print("\nAnomaly detection completed successfully.")


if __name__ == "__main__":
    run_anomaly_detection()