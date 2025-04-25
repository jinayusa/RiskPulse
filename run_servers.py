import subprocess
import asyncio

async def run_command(command):
    process = await asyncio.create_subprocess_shell(command)
    await process.communicate()

async def main():
    # Start FastAPI server
    fastapi_cmd = "uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
    consumer_cmd = "python -m app.kafka.consumer"
    
    # Kafka and MongoDB need to be running first
    kafka_cmd = "docker-compose up -d kafka"
    mongodb_cmd = "docker-compose up -d mongodb"

    # Running all services in parallel
    await asyncio.gather(
        run_command(kafka_cmd),
        run_command(mongodb_cmd),
        run_command(fastapi_cmd),
        run_command(consumer_cmd)
    )

if __name__ == "__main__":
    asyncio.run(main())
