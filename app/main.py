from fastapi import FastAPI
from app.routes import transactions

app = FastAPI(title="RiskPulse API")

app.include_router(transactions.router)
