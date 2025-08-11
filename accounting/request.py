import requests
import json

# Define the endpoint
url = "http://localhost:5000/process"

# Sample JSON payload
payload = {
    "statements": [
        {
            "account_name": "Participation Fees",
            "credit": 1500.00,
            "date": "2025-08-01"
        },
        {
            "account_name": "Tutor Fees",
            "credit": 800.00,
            "date": "2025-08-02"
        },
        {
            "account_name": "Donations",
            "credit": 500.00,
            "date": "2025-08-03"
        },
        {
            "account_name": "Event materials",
            "debit": 600.00,
            "source": "ABC Supplies",
            "original_price": 650.00,
            "discount": 50.00,
            "final_amount": 600.00,
            "date": "2025-08-04"
        },
                {
            "account_name": "Event materials",
            "debit": 600.00,
            "source": "ADEF Supplies",
            "original_price": 800.00,
            "discount": 00.00,
            "final_amount": 800.00,
            "date": "2025-08-04"
        },
        {
            "account_name": "Rent Expense",
            "debit": 1200.00,
            "source": "Venue Co.",
            "original_price": 1200.00,
            "discount": 0.00,
            "final_amount": 1200.00,
            "date": "2025-08-05"
        },
        {
            "account_name": "Refreshments",
            "debit": 300.00,
            "source": "Catering Ltd.",
            "original_price": 350.00,
            "discount": 50.00,
            "final_amount": 300.00,
            "date": "2025-08-06"
        }
    ]
}

# Send POST request
response = requests.post(url, json=payload)

# Save the response file
if response.status_code == 200:
    with open("Income_Statement_and_Cash_Book.xlsx", "wb") as f:
        f.write(response.content)
    print("✅ File downloaded successfully.")
else:
    print(f"❌ Request failed with status code {response.status_code}")