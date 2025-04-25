import datetime
from collections import defaultdict

# --- Memory Storage ---
user_last_transaction = {}
user_last_country = {}  # Memory to store the last country visited by the user

def evaluate_transaction(transaction: dict) -> (float, list):
    risk_score = 0.0
    triggered_rules = []

    # Rule 1: High Amount Rule
    if transaction.get("amount", 0) > 10000:
        risk_score += 0.5
        triggered_rules.append("High Amount Transaction")

    # Rule 2: Nighttime Transaction Rule
    timestamp = transaction.get("timestamp")
    if isinstance(timestamp, str):
        timestamp = datetime.datetime.fromisoformat(timestamp)

    if timestamp.hour >= 2 and timestamp.hour <= 5:
        risk_score += 0.2
        triggered_rules.append("Nighttime Transaction")

    # --- Multiple Countries Rule ---
    user_id = transaction.get("user_id")
    location = transaction.get("location")
    country = location.split(', ')[-1]  # Assuming format: 'City, Country'

    if user_id in user_last_country:
        last_country = user_last_country[user_id]
        last_txn_time = user_last_transaction[user_id]

        # If the transaction is in a new country
        if last_country != country:
            time_diff = (timestamp - last_txn_time).total_seconds() / 3600  # time in hours
            if time_diff < 1:  # Transactions within 1 hour in different countries
                risk_score += 0.4
                triggered_rules.append("Multiple Countries Detected")

    # Update memory for the user
    user_last_country[user_id] = country
    user_last_transaction[user_id] = timestamp

    # Ensure risk score is capped between 0 and 1
    risk_score = min(risk_score, 1.0)

    return risk_score, triggered_rules
