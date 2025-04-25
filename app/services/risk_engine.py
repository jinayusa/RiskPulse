import random

def calculate_risk_score(transaction):
    # Dummy risk scoring logic for now
    score = random.uniform(0, 1)
    is_fraud = score > 0.85
    return round(score, 4), is_fraud
