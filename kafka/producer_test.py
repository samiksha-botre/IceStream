from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda value: value.encode("utf-8")
)

message = "Hello from IceStream!"

producer.send("icestream-transactions", value=message)
producer.flush()

print("Message sent successfully!")