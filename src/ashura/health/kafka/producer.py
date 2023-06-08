import logging
from django.conf import settings
from confluent_kafka import Producer
from .serializer import serialize_message

logger = logging.getLogger("ashura_kafka_producer")

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class KafkaProducer(metaclass=Singleton):
    def __init__(self):
        self.producer = Producer({'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS})

    def send_message(self, topic, message):
        serialized_message = message

        try:
            self.producer.produce(topic, serialized_message.encode('utf-8'))
            self.producer.flush()
            logger.info(f'Message sent to Kafka: {serialized_message}')
        except Exception as e:
            logger.error(f'Error occurred while producing to Kafka: {e}')