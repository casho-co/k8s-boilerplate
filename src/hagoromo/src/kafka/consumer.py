import asyncio
import logging
import os
from .config import Topics
# from ..database import connect_to_mongo, disconnect_from_mongo
from ..database import MongoDBClient
from shared.async_helpers import AsyncKafkaConsumer

KAFKA_BROKER = os.environ.get('KAFKA_BROKER','kafka-service:9092')

# Define LOGGING configuration
LOG_LEVEL = logging.DEBUG

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'hagoromo_consumer': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
        'default': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
    },
    'root': {
        'handlers': [],
        'level': 'WARNING',
    },
}

# Setup logging
logging.config.dictConfig(LOGGING)
logger = logging.getLogger('default')

async def start_consumer():
    mongo_client = MongoDBClient()
    await mongo_client.db 
    kafka_consumer = AsyncKafkaConsumer(KAFKA_BROKER,"hagoromo_consumer_group")
    try:
        await kafka_consumer.subscribe([Topics.HEALTH.value])                    

    finally:
        await mongo_client.disconnect()     
        kafka_consumer.close()

if __name__ == "__main__":
    asyncio.run(start_consumer())