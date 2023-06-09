import { Kafka, Producer, ProducerRecord } from 'kafkajs';
import { IProducer } from '../interfaces/iproducer';
import { IEvent } from '../interfaces/ievent';
import { logger } from '../../lib/logger';

// Concrete implementation for a KafkaProducer
export class KafkaProducer implements IProducer {
  private static instance: KafkaProducer;
  private producer: Producer;

  private constructor(broker: string) {
    const kafka = new Kafka({
      brokers: [broker],
    });
    this.producer = kafka.producer();
  }

  public static getInstance(broker: string): IProducer {
    if (!KafkaProducer.instance) {
      KafkaProducer.instance = new KafkaProducer(broker);
    }
    return KafkaProducer.instance;
  }

  public sendMessage = async (topic: string, message: IEvent) => {
    await this.producer.connect();

    const now = new Date().toUTCString();
    message.createdAt = now;

    const event: ProducerRecord = {
      topic: topic,
      messages: [{ value: JSON.stringify(message) }],
    };

    await this.producer
      .send(event)
      .then(() => {
        logger.info(`Message sent to Kafka: ${JSON.stringify(message)}`);
      })
      .catch((err) => {
        logger.error(`Error occurred while producing to Kafka: ${err.message}`);
      });
  };
}
