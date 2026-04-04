import pandas as pd

data = {
    "loan_id": ["LN-5001","LN-5002","LN-5003","LN-5004","LN-5005"],
    "customer_id": ["CID-10001","CID-10001","CID-10002","CID-10003","CID-10003"],
    "borrower_name": ["Mehta Traders Pvt Ltd","Mehta Traders Pvt Ltd","Rajan Enterprises","Sunita Textiles","Sunita Textiles"],
    "pan": ["ABCDE1234F","ABCDE1234F","BCDEF2345G","CDEFG3456H","CDEFG3456H"],
    "phone": ["9876543210","9876543210","9765432109","9654321098","9654321098"],
    "product": ["Business Loan","Working Capital","MSME Loan","Equipment Finance","Business Loan"],
    "geography": ["Mumbai","Mumbai","Pune","Nagpur","Nagpur"],
    "disbursement_date": ["2024-01-15","2023-06-10","2024-02-10","2023-11-05","2024-03-20"],
    "loan_amount": [500000,200000,300000,1000000,400000],
    "outstanding_amount": [420000,80000,180000,850000,350000],
    "tenure_months": [36,12,24,48,24],
    "interest_rate": [18.5,20.0,16.0,14.5,17.5],
    "emis_paid": [8,10,6,12,4],
    "dpd": [0,0,30,90,0],
    "bucket": ["Current","Current","SMA-0","SMA-2","Current"],
    "collection_status": ["Collected","Collected","Partially Collected","Partially Collected","Collected"],
    "bureau_score_at_origination": [720,720,680,750,750]
}

df = pd.DataFrame(data)
df.to_csv("sample_upload.csv", index=False)
print("Sample file created with customer_id, PAN and phone columns")
print(df[["customer_id","loan_id","borrower_name","product","bucket"]].to_string())