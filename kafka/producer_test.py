import json
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)

message = {
    "transaction_id": "KAFKA001",
    "user_id": "USER001",
    "product": "Laptop",
    "amount": 50000,
    "tax_amount": 9000,
    "payment_method": "UPI",
    "status": "SUCCESS",
    "timestamp": "2026-09-16T12:30:00"
}

producer.send("icestream-transactions", value=message)
producer.flush()

print("Transaction sent successfully!")