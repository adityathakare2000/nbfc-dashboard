import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

random.seed(42)
np.random.seed(42)

first_names = [
    "Aarav","Vivaan","Aditya","Rahul","Rohit","Amit","Suresh","Vijay","Raj","Sanjay",
    "Priya","Ananya","Pooja","Sneha","Neha","Divya","Kavya","Meera","Ishita","Riya",
    "Ravi","Ramesh","Mahesh","Ganesh","Dinesh","Naresh","Mukesh","Rakesh","Rajesh","Manoj",
    "Fatima","Ayesha","Zara","Sana","Noor","Thomas","Joseph","James","John","Robert",
    "Lakshmi","Saraswati","Parvati","Radha","Ganga","Dhruv","Kabir","Arjun","Ishaan","Shaurya"
]

last_names = [
    "Sharma","Verma","Gupta","Singh","Kumar","Patel","Shah","Mehta","Joshi","Trivedi",
    "Agarwal","Mishra","Pandey","Tiwari","Chauhan","Yadav","Dubey","Shukla","Srivastava","Pathak",
    "Nair","Pillai","Menon","Iyer","Reddy","Rao","Naidu","Murthy","Chatterjee","Banerjee",
    "Desai","Jain","Kothari","Parekh","Gandhi","Kaur","Bhatia","Malhotra","Chopra","Kapoor",
    "Khan","Ahmed","Ansari","Siddiqui","Fernandes","DSouza","Pereira","Nagarajan","Venkatesh","Balakrishnan"
]

suffixes = ["Pvt Ltd","Enterprises","Traders","Industries","Solutions","Agency","Associates","Brothers","Co","Works"]

products = ["Business Loan","MSME Loan","Equipment Finance","Working Capital","Personal Loan"]
product_weights = [0.30, 0.25, 0.15, 0.20, 0.10]
geographies = ["Mumbai","Pune","Nagpur","Nashik","Aurangabad","Thane","Kolhapur","Delhi","Bengaluru","Hyderabad"]

def random_date(start, end):
    return (start + timedelta(days=random.randint(0, (end-start).days))).strftime("%Y-%m-%d")

def get_bucket(dpd):
    if dpd == 0: return "Current"
    elif dpd <= 30: return "SMA-0"
    elif dpd <= 60: return "SMA-1"
    elif dpd <= 90: return "SMA-2"
    else: return "NPA"

def generate_pan():
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return f"{''.join(random.choices(letters, k=5))}{random.randint(1000,9999)}{''.join(random.choices(letters, k=1))}"

def generate_phone():
    return f"9{random.randint(100000000, 999999999)}"

NUM_CUSTOMERS = 200
customers = []
used_names = set()
used_pans = set()

for i in range(NUM_CUSTOMERS):
    fn = random.choice(first_names)
    ln = random.choice(last_names)
    sf = random.choice(suffixes)
    name = f"{fn} {ln} {sf}"
    counter = 1
    while name in used_names:
        name = f"{fn} {ln} {sf} {counter}"
        counter += 1
    used_names.add(name)

    pan = generate_pan()
    while pan in used_pans:
        pan = generate_pan()
    used_pans.add(pan)

    customers.append({
        "customer_id": f"CID-{10000+i}",
        "borrower_name": name,
        "pan": pan,
        "phone": generate_phone(),
        "geography": random.choice(geographies),
    })

customers_df = pd.DataFrame(customers)

loan_records = []
loan_counter = 0
disbursement_start = datetime(2022, 1, 1)
disbursement_end = datetime(2024, 6, 30)

for _, customer in customers_df.iterrows():
    num_loans = random.choices([1, 2, 3], weights=[0.60, 0.30, 0.10])[0]
    for _ in range(num_loans):
        loan_amount = int(random.choice([100000,200000,300000,500000,750000,1000000,1500000,2000000]))
        tenure = int(random.choice([12,24,36,48,60]))
        interest_rate = round(random.uniform(12, 24), 2)
        dpd = int(np.random.choice([0,0,0,0,0,15,30,45,60,75,90,120], p=[0.30,0.15,0.15,0.10,0.07,0.06,0.05,0.04,0.03,0.02,0.02,0.01]))
        emis_paid = int(tenure * random.uniform(0.2, 0.9))
        outstanding = round(loan_amount * random.uniform(0.3, 0.95), 0)
        bucket = get_bucket(dpd)
        collection_status = "Collected" if dpd == 0 else "Partially Collected" if dpd <= 60 else "Defaulted"
        bureau_score = random.randint(550, 850)

        loan_records.append({
            "loan_id": f"LN-{20000+loan_counter}",
            "customer_id": customer["customer_id"],
            "borrower_name": customer["borrower_name"],
            "pan": customer["pan"],
            "phone": customer["phone"],
            "product": np.random.choice(products, p=product_weights),
            "geography": customer["geography"],
            "disbursement_date": random_date(disbursement_start, disbursement_end),
            "loan_amount": loan_amount,
            "outstanding_amount": outstanding,
            "tenure_months": tenure,
            "interest_rate": interest_rate,
            "emis_paid": emis_paid,
            "dpd": dpd,
            "bucket": bucket,
            "collection_status": collection_status,
            "bureau_score_at_origination": bureau_score
        })
        loan_counter += 1

loans_df = pd.DataFrame(loan_records)
loans_df.to_csv("loan_portfolio.csv", index=False)

print(f"Generated {len(customers_df)} unique customers")
print(f"Generated {len(loans_df)} loan records")
print(f"\nCustomers with multiple loans: {len(loans_df.groupby('customer_id').filter(lambda x: len(x) > 1)['customer_id'].unique())}")
print(f"\nBucket distribution:")
print(loans_df["bucket"].value_counts())
print(f"\nTotal AUM: Rs.{loans_df['outstanding_amount'].sum()/10000000:.1f} Cr")
print(f"\nSample customer with multiple loans:")
multi = loans_df.groupby("customer_id").filter(lambda x: len(x) > 1)
if len(multi) > 0:
    sample_cid = multi["customer_id"].iloc[0]
    print(loans_df[loans_df["customer_id"] == sample_cid][["customer_id","loan_id","borrower_name","product","outstanding_amount","bucket"]])