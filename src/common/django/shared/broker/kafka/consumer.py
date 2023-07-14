import logging
import json
from typing import List, Callable
from confluent_kafka import Consumer
from ..interfaces.ievent import IEvent 
from ..interfaces.iconsumer import  IConsumer
from ..registry import topics_registry

logger = logging.getLogger('default')

class KafkaConsumer(IConsumer):
    def __init__(self, broker: str, consumer_group: str):
        self.consumer = Consumer({
            'bootstrap.servers': broker,
            'group.id': consumer_group,
            'auto.offset.reset': 'earliest'
        })

    def subscribe(self, topics: list[str]) -> None:
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
            event_message = IEvent().from_dict(deserialized_message)
            message_topic = message.topic()
            logger.info(
                f"Message received: "
                f"topic: {message_topic}, "
                f"event: {event_message.eventType}, "
                f"data: {event_message.data}, "
                f"createdAt: {event_message.createdAt}"
            )
            if message.topic() in topics_registry:
                event_class = topics_registry[message_topic]
                function_name = f"consume_{event_message.eventType}"
                
                if hasattr(event_class, function_name) and callable(getattr(event_class, function_name)):
                    getattr(event_class, function_name)(event_message)
                else:
                    logger.info(f"Event type {event_message.eventType} is not handled by this consumer")
            else:
                logger.info(f"Topic {message_topic} is not handled by this consumer")

    def close(self):
        self.consumer.close()     
        