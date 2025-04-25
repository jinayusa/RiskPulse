from confluent_kafka import Producer
import json

# Kafka configuration
conf = {
    'bootstrap.servers': 'localhost:9092',  # Kafka broker
}

producer = Producer(**conf)

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result. """
    if err is not None:
        print(f"Delivery failed for record {msg.key()}: {err}")
    else:
        print(f"Record {msg.key()} successfully produced to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

import json

def send_transaction_to_kafka(transaction: dict):
    """ Publishes a transaction event to Kafka. """

    # Fix datetime to string
    if hasattr(transaction.get("timestamp"), 'isoformat'):
        transaction["timestamp"] = transaction["timestamp"].isoformat()

    producer.produce(
        topic='transactions_stream',
        key=transaction["transaction_id"],
        value=json.dumps(transaction),
        callback=delivery_report
    )
    producer.flush()
