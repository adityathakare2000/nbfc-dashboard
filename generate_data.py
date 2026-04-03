import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

random.seed(42)
np.random.seed(42)

n = 10000

loan_ids = [f"LN-{10000 + i}" for i in range(n)]

products = ["Business Loan", "MSME Loan", "Equipment Finance", "Working Capital", "Personal Loan"]
product_weights = [0.30, 0.25, 0.15, 0.20, 0.10]

geographies = ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad", "Thane", "Kolhapur"]

borrower_names = [
    "Mehta Traders", "Rajan Enterprises", "Sunita Textiles", "Kumar Auto Parts",
    "Priya Foods", "Sharma Electronics", "Patel Hardware", "Singh Pharma",
    "Gupta Garments", "Desai Construction", "Joshi Logistics", "Verma Agro",
    "Nair Exports", "Iyer Chemicals", "Reddy Steel"
]

disbursement_start = datetime(2023, 1, 1)
disbursement_end = datetime(2024, 6, 30)

def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

disbursement_dates = [random_date(disbursement_start, disbursement_end) for _ in range(n)]

loan_amounts = np.random.choice(
    [100000, 200000, 300000, 500000, 750000, 1000000, 1500000, 2000000],
    size=n,
    p=[0.10, 0.15, 0.20, 0.20, 0.15, 0.10, 0.07, 0.03]
)

tenures = np.random.choice([12, 24, 36, 48, 60], size=n, p=[0.10, 0.25, 0.35, 0.20, 0.10])

interest_rates = np.round(np.random.uniform(12, 24, n), 2)

dpd_values = np.random.choice(
    [0, 0, 0, 0, 0, 15, 30, 45, 60, 75, 90, 120],
    size=n,
    p=[0.30, 0.15, 0.15, 0.10, 0.07, 0.06, 0.05, 0.04, 0.03, 0.02, 0.02, 0.01]
)

def get_bucket(dpd):
    if dpd == 0:
        return "Current"
    elif dpd <= 30:
        return "SMA-0"
    elif dpd <= 60:
        return "SMA-1"
    elif dpd <= 90:
        return "SMA-2"
    else:
        return "NPA"

buckets = [get_bucket(d) for d in dpd_values]

outstanding = np.round(loan_amounts * np.random.uniform(0.3, 0.95, n), 0)

emis_paid = (tenures * np.random.uniform(0.2, 0.9, n)).astype(int)

collection_status = ["Collected" if d == 0 else "Partially Collected" if d <= 60 else "Defaulted" for d in dpd_values]

bureau_scores = np.random.choice(
    range(550, 850),
    size=n
)

df = pd.DataFrame({
    "loan_id": loan_ids,
    "borrower_name": [random.choice(borrower_names) + f" {random.randint(1,99)}" for _ in range(n)],
    "product": np.random.choice(products, size=n, p=product_weights),
    "geography": np.random.choice(geographies, size=n),
    "disbursement_date": disbursement_dates,
    "loan_amount": loan_amounts,
    "outstanding_amount": outstanding,
    "tenure_months": tenures,
    "interest_rate": interest_rates,
    "emis_paid": emis_paid,
    "dpd": dpd_values,
    "bucket": buckets,
    "collection_status": collection_status,
    "bureau_score_at_origination": bureau_scores
})

df.to_csv("loan_portfolio.csv", index=False)
print("Done! loan_portfolio.csv created with", len(df), "loan records.")
print("\nQuick summary:")
print(df["bucket"].value_counts())
print(f"\nTotal AUM: ₹{df['outstanding_amount'].sum()/10000000:.2f} Cr")