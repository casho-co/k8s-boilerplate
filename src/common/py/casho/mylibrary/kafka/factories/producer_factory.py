from ..interfaces import IProducer, IProducerConfiguration
from ..Kafka_implementation.kafka_producer import KafkaProducer

class ProducerFactory:
    kafka_producers = {}

    @staticmethod
    def get_producer(metadata: IProducerConfiguration) -> IProducer or None:
        if metadata.type == "Kafka":
            return ProducerFactory.get_kafka_producer(metadata.broker)
        return None

    @staticmethod
    def get_kafka_producer(broker: str) -> IProducer:
        if broker in ProducerFactory.kafka_producers:
            return ProducerFactory.kafka_producers[broker]
        else:
            producer = KafkaProducer.get_instance(broker)
            ProducerFactory.kafka_producers[broker] = producer
            return producer
