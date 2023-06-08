from django.core.management.base import BaseCommand
from health.kafka_utils import KafkaConsumer

class Command(BaseCommand):
    help = "Starts the Kafka consumer"
    def handle(self, *args, **options):
        consumer = KafkaConsumer()
        try:
            consumer.process_messages()
        finally:
            consumer.close()
