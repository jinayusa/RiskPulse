from fastapi import APIRouter, HTTPException
from app.models import Transaction, RiskScoreResponse
from app.kafka.producer import send_transaction_to_kafka
from app.database.mongo_client import transactions_collection
import json

router = APIRouter()

@router.post("/transaction", response_model=RiskScoreResponse)
def ingest_transaction(transaction: Transaction):
    transaction_dict = transaction.dict()

    # Send transaction to Kafka instead of storing
    send_transaction_to_kafka(transaction_dict)

    # Dummy immediate response (Kafka consumer will handle real risk scoring)
    return RiskScoreResponse(
        transaction_id=transaction.transaction_id,
        risk_score=0.0,  # Real score will come from consumer later
        is_fraud=False
    )
@router.get("/risk_score/{transaction_id}", response_model=RiskScoreResponse)
def get_risk_score(transaction_id: str):
    transaction = transactions_collection.find_one({"transaction_id": transaction_id})

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return RiskScoreResponse(
        transaction_id=transaction_id,
        risk_score=transaction["risk_score"],
        is_fraud=transaction["is_fraud"]
    )
