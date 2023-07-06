import logging
from typing import Callable
from confluent_kafka import Consumer
from .serializer import deserialize_message

logger = logging.getLogger()

class KafkaConsumer:

    def __init__(self,bootstrap_servers: str, group_id: str):
        self.consumer = Consumer({
            'bootstrap.servers':bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest'
        })

def subscribe(self, topic: str, callback: Callable[[dict], None]) -> None:
        self.consumer.subscribe(topics=[topic])

        while True:
            message = self.consumer.poll(1.0)
            if message is None:
                continue
            if message.error():
                logger.error(
                    f'Error occurred while consuming from Kafka: {message.error().str()}')
                continue
            json_message = deserialize_message(message.value().decode('utf-8'))
            callback(json_message)
            logger.info(f"Received Message on Common Django: {json_message}")

def close(self):
    self.consumer.close()
