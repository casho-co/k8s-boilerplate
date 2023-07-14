import logging
from shared.broker import IEvent, register_topic
from kafka.config import Topics

logger = logging.getLogger("ashura_app")

@register_topic(Topics.HEALTH.value)
class Health:
    
    @staticmethod
    def produce_check_health():
        return 'check_health'
    
    @staticmethod
    def consume_check_health(message: IEvent):
        logger.info("Message received by handler: %s", message.data)