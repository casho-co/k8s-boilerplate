from datetime import datetime
import logging
import uuid
from shared.broker import IEvent, register_topic
from ...database import MongoDBClient

from ..config import Topics
logger = logging.getLogger("hagoromo_consumer")

mongo_client = MongoDBClient()


@register_topic(Topics.HEALTH.value)
class Health:
    
    @staticmethod
    def produce_check_health():
        return 'CHECK_HEALTH'
    
    @staticmethod
    async def consume_check_health(message: IEvent):
        db = await mongo_client.db
        await db['users'].insert_one({'id':str(uuid.uuid4()),'name':'test','created_at': datetime.now()})
        logger.info("Message received by handler: %s", message.data)