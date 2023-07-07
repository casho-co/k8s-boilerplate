import logging
from confluent_kafka import Producer
from .serializer import serialize_message

logger = logging.getLogger()


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class KafkaProducer(metaclass=Singleton):
    def __init__(self,broker: str):
        self.producer = Producer(
            {'bootstrap.servers': broker})

    def acked(self, err, msg):
        if err is not None:}: {err.str()}')
            logger.error(
                f'Failed to deliver message: {msg.value()
        else:
            logger.info(f'Message produced: {msg.value()}')

    def send_message(self, topic, message):
        serialized_message = serialize_message(message)

        try:
            self.producer.produce(topic, serialized_message.encode(
                'utf-8'), callback=self.acked)
            self.producer.flush()
        except Exception as e:
            logger.error(f'Error occurred while producing to Kafka: {e}')
