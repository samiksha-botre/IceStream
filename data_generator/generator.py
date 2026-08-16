import random
import time
from datetime import datetime


products = ["Laptop", "Mobile", "Headphones", "Keyboard", "Mouse"]
payment_methods = ["UPI", "Credit Card", "Debit Card", "Cash"]
statuses = ["SUCCESS", "FAILED", "PENDING"]


def generate_transaction():
    transaction = {
        "transaction_id": f"TXN{random.randint(100000, 999999)}",
        "user_id": f"USR{random.randint(1000, 9999)}",
        "product": random.choice(products),
        "amount": random.randint(100, 100000),
        "tax_amount": random.randint(10, 20000),
        "payment_method": random.choice(payment_methods),
        "status": random.choice(statuses),
        "timestamp": datetime.now().isoformat()
    }

    # Inject bad data occasionally
    if random.random() < 0.05:
        bad_field = random.choice(["amount", "tax_amount"])
        transaction[bad_field] = None

    # Inject schema drift occasionally
    if random.random() < 0.02:
        transaction["discount"] = random.randint(1, 50)
        
    return transaction


while True:
    transaction = generate_transaction()
    print(transaction)

    time.sleep(0.01)