from ..interfaces import IConsumer, ConsumerConfiguration
from ..Kafka_implementation.kafka_consumer import KafkaConsumer

class ConsumerFactory:
    @staticmethod
    def get_consumer(metadata: ConsumerConfiguration) -> IConsumer or None:
        if metadata.type == "Kafka":
            return KafkaConsumer(metadata.broker,metadata.consumer_group)
        return None