import logging
from django.core.management.base import BaseCommand
from shared.broker.interfaces import IEvent
from shared.broker.kafka import KafkaConsumer
from django.conf import settings

logger = logging.getLogger("ashura_consumer")

def callback(event: IEvent):
    logger.info("Received event: %s", event.data)


class Command(BaseCommand):
    help = "Starts the Kafka consumer"

    def handle(self, *args, **options):
        consumer = KafkaConsumer(settings.KAFKA_BROKER, "health_consumer_group_node")
        try:
            consumer.subscribe(settings.TOPIC_HEALTH, callback)
        finally:
            consumer.close()