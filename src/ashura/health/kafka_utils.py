from confluent_kafka import Consumer, Producer
from django.conf import settings

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
                print(f'Error occurred while consuming from Kafka: {message.error().str()}')
                continue
            print(f'Received message: {message.value().decode("utf-8")}')
            # Process the message as needed

    def close(self):
        self.consumer.close()
        
        
class KafkaProducer(metaclass=Singleton):
    def __init__(self):
        self.producer = Producer({'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS})

    def send_message(self, message):
        self.producer.produce('health', message.encode('utf-8'))
        print("yeaa flushing")
        self.producer.flush()
        print("yes flushed")

