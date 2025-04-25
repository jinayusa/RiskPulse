import datetime
from collections import defaultdict
from geopy.distance import geodesic

# --- Existing ---
user_last_transaction = {}
user_transaction_times = defaultdict(list)  # ✅ NEW memory for burst detection

def evaluate_transaction(transaction: dict) -> (float, list):
    risk_score = 0.0
    triggered_rules = []

    # -- High Amount Rule --
    if transaction.get("amount", 0) > 10000:
        risk_score += 0.5
        triggered_rules.append("High Amount Transaction")

    # -- Nighttime Rule --
    timestamp = transaction.get("timestamp")
    if isinstance(timestamp, str):
        timestamp = datetime.datetime.fromisoformat(timestamp)

    if 2 <= timestamp.hour <= 5:
        risk_score += 0.2
        triggered_rules.append("Nighttime Transaction")

    # -- Geo-Velocity Rule --
    user_id = transaction.get("user_id")
    location = transaction.get("location")

    if user_id in user_last_transaction:
        last_txn = user_last_transaction[user_id]
        last_location = last_txn["location"]
        last_time = last_txn["timestamp"]

        if location != last_location:
            time_diff = (timestamp - last_time).total_seconds() / 3600  # in hours
            distance = 8000  # Assume very long distance between cities

            if time_diff < 5 and distance / time_diff > 500:
                risk_score += 0.3
                triggered_rules.append("Unrealistic Geo-Velocity")

    user_last_transaction[user_id] = {
        "location": location,
        "timestamp": timestamp
    }

    # --- Transaction Burst Rule ---
    transaction_times = user_transaction_times[user_id]

    # Add current transaction time
    transaction_times.append(timestamp)

    # Only keep transactions within last 2 minutes
    two_minutes_ago = timestamp - datetime.timedelta(minutes=2)
    transaction_times = [t for t in transaction_times if t > two_minutes_ago]

    user_transaction_times[user_id] = transaction_times  # update cleaned list

    if len(transaction_times) >= 3:
        risk_score += 0.4
        triggered_rules.append("Transaction Burst Detected")

    # -- Cap the risk score --
    risk_score = min(risk_score, 1.0)

    return risk_score, triggered_rules
