#!/bin/bash

# Start MongoDB
echo "Starting MongoDB..."
docker-compose up -d mongodb

# Start Zookeeper
echo "Starting Zookeeper..."
docker-compose up -d zookeeper

# Start Kafka
echo "Starting Kafka..."
docker-compose up -d kafka

# Start FastAPI (ensure you're in the correct environment, and FastAPI is already set up)
echo "Starting FastAPI..."
# Activate your virtual environment
source .venv/bin/activate
# Run FastAPI server
uvicorn app.main:app --reload &

# Start Kafka Consumer in the background
echo "Starting Kafka Consumer..."
python -m app.kafka.consumer &

echo "All services started successfully!"
