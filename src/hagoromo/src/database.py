import logging
import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING
from shared.decorators import singleton

MONGO_INITDB_ROOT_USERNAME = os.environ.get("MONGO_INITDB_ROOT_USERNAME", "hagoromo-user")
MONGO_INITDB_ROOT_PASSWORD = os.environ.get("MONGO_INITDB_ROOT_PASSWORD", "password")
MONGO_HOST = os.environ.get("MONGO_HOST", "localhost")
MONGO_PORT = os.environ.get("MONGO_PORT", "27017")
MONGO_INITDB_DATABASE = os.environ.get("MONGO_INITDB_DATABASE", "hagoromo-db")

logger = logging.getLogger('default')

@singleton
class MongoDBClient:
    def __init__(self):
        self._uri = self._uri = (
            f"mongodb://{MONGO_INITDB_ROOT_USERNAME}:"
            f"{MONGO_INITDB_ROOT_PASSWORD}@"
            f"{MONGO_HOST}:{MONGO_PORT}/"
            f"{MONGO_INITDB_DATABASE}?authSource=admin"
        )
        self._db_name = MONGO_INITDB_DATABASE
        self._client = None
        self._db = None

    async def _connect(self):
        if self._client is None:
            self._client = AsyncIOMotorClient(self._uri)
            self._db = self._client.get_database(self._db_name)
            users = self._db.get_collection("users")
            ping_response = await self._db.command("ping")
            if int(ping_response["ok"]) != 1:
                raise Exception("Problem connecting to database cluster.")
            else:
                logger.info("Connected to database.")
                await users.create_index([("name", ASCENDING)], unique=True)

    async def disconnect(self):
        if self._client:
            self._client.close()
            logger.info("Disconnected from MongoDB.")
            self._client = None
            self._db = None

    @property
    async def db(self):
        if self._db is None:
            await self._connect()
        return self._db