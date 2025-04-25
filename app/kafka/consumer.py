from confluent_kafka import Consumer
import json
from app.storage import transaction_db, risk_scores
from app.services.geo_velocity_rule_engine import evaluate_transaction
from app.database.mongo_client import transactions_collection

# Kafka Consumer Configuration
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'riskpulse-consumer-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['transactions_stream'])

print("RiskPulse Consumer started. Listening for transactions...")

try:
    while True:
        msg = consumer.poll(1.0)  # Wait up to 1 second for new message
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        # Deserialize transaction message
        transaction_data = json.loads(msg.value().decode('utf-8'))

        transaction_id = transaction_data["transaction_id"]
        print(f"Received Transaction ID: {transaction_id}")

        # Store raw transaction temporarily in memory
        transaction_db[transaction_id] = transaction_data

        # Evaluate transaction using rule engine
        score, triggered_rules = evaluate_transaction(transaction_data)

        # Determine fraud status
        is_fraud = score > 0.85  # Using 85% risk score threshold for now

        # Save risk scoring result temporarily in memory
        risk_scores[transaction_id] = {
            "score": score,
            "is_fraud": is_fraud
        }

        try:
            result = transactions_collection.insert_one({
                "transaction_id": transaction_id,
                "transaction": transaction_data,
                "risk_score": score,
                "is_fraud": is_fraud,
                "triggered_rules": triggered_rules
            })
            print(f"Inserted transaction {transaction_id} with result: {result.inserted_id}")
        except Exception as e:
            print(f"Error inserting transaction {transaction_id} into MongoDB: {e}")

except KeyboardInterrupt:
    pass
finally:
    consumer.close()
