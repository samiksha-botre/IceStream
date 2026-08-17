import random
import time
import json
from datetime import datetime
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)


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

    producer.send("icestream-transactions", value=transaction)
    print("Sent:", transaction)

    time.sleep(0.01)