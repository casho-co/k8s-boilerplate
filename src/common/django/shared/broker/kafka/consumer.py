import logging
import json
from typing import List, Callable
from confluent_kafka import Consumer
from ..interfaces.ievent import IEvent 
from ..interfaces.iconsumer import  IConsumer

logger = logging.getLogger()

class KafkaConsumer(IConsumer):
    def __init__(self, broker: str, consumer_group: str):
        self.consumer = Consumer({
            'bootstrap.servers': broker,
            'group.id': consumer_group,
            'auto.offset.reset': 'earliest'
        })

    def subscribe(self, topics: list[str],  callback: Callable[[IEvent], None]) -> None:
        self.consumer.subscribe(topics=topics)
                    
        while True:
            message = self.consumer.poll(1.0)
            if message is None:
                continue
            if message.error():
                logger.error(
                    f'Error occurred while consuming from Kafka: {message.error().str()}')
                continue
            deserialized_message = json.loads(message.value().decode('utf-8'))
            
            callback(message.topic(), deserialized_message)
            logger.info(f"Message sent to callback : {deserialized_message}")

    def close(self):
        self.consumer.close()     
        