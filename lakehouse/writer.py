import sys
import json
import os

sys.path.insert(0, r"C:\IceStream")

from lakehouse.config import get_lakehouse_path

def write_valid_transaction(transaction, status):
    if status == "VALID":
        write_transaction(transaction)

def write_transaction(transaction):
    lakehouse_path = get_lakehouse_path()

    os.makedirs(lakehouse_path, exist_ok=True)

    output_file = os.path.join(
        lakehouse_path,
        "transactions.jsonl"
    )

    with open(output_file, "a", encoding="utf-8") as file:
        file.write(json.dumps(transaction) + "\n")


if __name__ == "__main__":
    sample_transaction = {
        "transaction_id": "TEST001",
        "user_id": "USER001",
        "product": "Laptop",
        "amount": 50000,
        "tax_amount": 9000,
        "payment_method": "UPI",
        "status": "SUCCESS",
        "timestamp": "2026-09-15T12:00:00"
    }

    write_transaction(sample_transaction)

    print("Transaction written to lakehouse.")