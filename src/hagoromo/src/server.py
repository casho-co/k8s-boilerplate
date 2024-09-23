from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import MongoDBClient
# from .database import connect_to_mongo, disconnect_from_mongo
from .api import api_router
from .kafka.events import *
from shared.broker import KafkaProducer
import logging
import logging.config
import os

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
        'hagoromo_app': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
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

@asynccontextmanager
async def lifespan(app: FastAPI):
    mongo_client = MongoDBClient()
    app.db = await mongo_client.db
    yield 
    await mongo_client.disconnect()

app: FastAPI = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.kafka_producer = KafkaProducer(KAFKA_BROKER)

app.include_router(api_router, prefix='/api/hagoromo')
