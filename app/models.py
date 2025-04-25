from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Transaction(BaseModel):
    transaction_id: str
    user_id: str
    card_number: str
    amount: float
    location: str
    timestamp: datetime

class RiskScoreResponse(BaseModel):
    transaction_id: str
    risk_score: float
    is_fraud: bool
