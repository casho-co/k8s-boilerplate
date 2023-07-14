import logging
from django.core.management.base import BaseCommand
from shared.broker.kafka import KafkaConsumer
from django.conf import settings
from kafka.config import Topics

logger = logging.getLogger("ashura_consumer")


class Command(BaseCommand):
    help = "Starts the Kafka consumer"

    def handle(self, *args, **options):
        consumer = KafkaConsumer(settings.KAFKA_BROKER, "ashura_health_group")
        try:
            consumer.subscribe([Topics.HEALTH.value])
        finally:
            consumer.close()