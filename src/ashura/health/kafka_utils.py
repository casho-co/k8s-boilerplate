import logging
from django.conf import settings
from confluent_kafka import Consumer, Producer

logger = logging.getLogger("ashura_kafka")

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class KafkaConsumer:
    def __init__(self):
        self.consumer = Consumer({
            'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS,
            'group.id': 'health_consumer_group',
            'auto.offset.reset': 'earliest'
        })
        self.consumer.subscribe(['health'])

    def process_messages(self):
        while True:
            message = self.consumer.poll(1.0)
            if message is None:
                continue
            if message.error():
                logger.error(f'Error occurred while consuming from Kafka: {message.error().str()}')
                continue
            logger.info(f'Received message: {message.value().decode("utf-8")}')
            # Process the message as needed

    def close(self):
        self.consumer.close()
        
        
class KafkaProducer(metaclass=Singleton):
    def __init__(self):
        self.producer = Producer({'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS})

    def send_message(self, message):
        try:
            self.producer.produce('health', message.encode('utf-8'))
            self.producer.flush()
            logger.info(f'Message sent to Kafka: {message}')
        except Exception as e:
            logger.error(f'Error occurred while producing to Kafka: {e}')

