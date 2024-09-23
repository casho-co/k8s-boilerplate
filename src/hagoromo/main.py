import argparse
import asyncio
import uvicorn
from src.kafka.consumer import start_consumer


# Argument parsing function to handle "app" or "consumer" modes
def parse_args():
    parser = argparse.ArgumentParser(description="Start the application")
    parser.add_argument(
        "mode", choices=["app", "consumer"], help="Run FastAPI app or Kafka consumer"
    )
    return parser.parse_args()

def main():
    args = parse_args()

    if args.mode == "app":
        # Run FastAPI app
        uvicorn.run("src.server:app", host="0.0.0.0", port=8010, reload=True)
    elif args.mode == "consumer":
        # Run Kafka consumer
        asyncio.run(start_consumer())  


if __name__ == "__main__":
    main()