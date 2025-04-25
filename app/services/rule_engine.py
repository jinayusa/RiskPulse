import datetime
from collections import defaultdict

# --- Memory Storage ---
user_spending_history = defaultdict(list)  # Tracks user spending over the past week

def evaluate_transaction(transaction: dict) -> (float, list):
    risk_score = 0.0
    triggered_rules = []

    # Rule 1: High Amount Rule
    if transaction.get("amount", 0) > 100:
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

    # (Assume you've already implemented and added other rules)

    # --- Behavioral Spending Spike Rule ---
    amount_spent = transaction.get("amount", 0)
    current_time = timestamp

    # Track user spending in the past week
    user_spending_history[user_id].append({
        "amount": amount_spent,
        "time": current_time
    })

    # Remove transactions older than 1 week
    one_week_ago = current_time - datetime.timedelta(weeks=1)
    user_spending_history[user_id] = [txn for txn in user_spending_history[user_id] if txn["time"] > one_week_ago]

    # Calculate average spending in the last week
    if len(user_spending_history[user_id]) > 0:
        avg_spending = sum(txn["amount"] for txn in user_spending_history[user_id]) / len(user_spending_history[user_id])

        print(f"User {user_id} spending history (last week): {user_spending_history[user_id]}")
        print(f"Average Spending: {avg_spending}")
        print(f"Current Transaction Amount: {amount_spent}")

        # Check for spending spike (5x-10x more than usual)
        if amount_spent >= 5 * avg_spending:
            risk_score += 0.5
            triggered_rules.append("Behavioral Spending Spike")
            print(f"Spending spike detected! Amount spent: {amount_spent}, Average: {avg_spending}")

    # Ensure risk score is capped between 0 and 1
    risk_score = min(risk_score, 1.0)

    print(f"Final Risk Score: {risk_score}")
    return risk_score, triggered_rules
