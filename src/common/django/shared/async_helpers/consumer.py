import logging
import json
from typing import List, Callable
from confluent_kafka import Consumer
from ..broker.interfaces.ievent import IEvent 
from ..broker.interfaces.iconsumer import  IConsumer
from ..broker.registry import topics_registry

logger = logging.getLogger('default')

class AsyncKafkaConsumer(IConsumer):
    def __init__(self, broker: str, consumer_group: str):
        self.consumer = Consumer({
            'bootstrap.servers': broker,
            'group.id': consumer_group,
            'auto.offset.reset': 'earliest'
        })

    async def subscribe(self, topics: list[str]) -> None:
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
                f"event: {event_message.event_type}, "
                f"data: {event_message.data}, "
                f"created_at: {event_message.created_at}"
            )
            if message.topic() in topics_registry:
                event_class = topics_registry[message_topic]
                function_name = f"consume_{event_message.event_type.lower()}"

                if hasattr(event_class, function_name) and callable(getattr(event_class, function_name)):
                    await getattr(event_class, function_name)(event_message)
                else:
                    logger.info(
                        f"Event type {event_message.event_type} is not handled by this consumer"
                    )
            else:
                logger.info(
                    f"Topic {message_topic} is not handled by this consumer"
                )

    def close(self):
        self.consumer.close()     
        