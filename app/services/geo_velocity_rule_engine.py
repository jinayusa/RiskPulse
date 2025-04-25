import datetime
from geopy.distance import geodesic  # we'll use it for real distance calculations later

# Dummy database to simulate user's last known location + time
# In real system this would come from user transaction history
user_last_transaction = {}

def evaluate_transaction(transaction: dict) -> (float, list):
    """
    Evaluate transaction against advanced fraud detection rules.
    Returns a tuple: (risk_score, list_of_triggered_rules)
    """

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

    # --- Advanced Rule: Geo-Velocity Check ---
    user_id = transaction.get("user_id")
    location = transaction.get("location")  # format: "City, Country"

    if user_id in user_last_transaction:
        last_txn = user_last_transaction[user_id]
        last_location = last_txn["location"]
        last_time = last_txn["timestamp"]

        # Calculate distance between two locations (very rough estimate)
        # Later we will simulate lat-long for precision
        # For now assume different cities imply 8000km+ travel
        if location != last_location:
            time_diff = (timestamp - last_time).total_seconds() / 3600  # hours
            distance = 8000  # fake large distance for city-to-city

            if time_diff < 5 and distance / time_diff > 500:  # unrealistic >500 km/hr
                risk_score += 0.3
                triggered_rules.append("Unrealistic Geo-Velocity")

    # Update user last transaction info
    user_last_transaction[user_id] = {
        "location": location,
        "timestamp": timestamp
    }

    # Ensure risk score capped
    risk_score = min(risk_score, 1.0)

    return risk_score, triggered_rules
