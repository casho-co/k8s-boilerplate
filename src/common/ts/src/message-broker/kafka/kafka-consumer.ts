import { logger } from '@cashoco/common';
import { Kafka } from 'kafkajs';
import { IConsumer } from '../interfaces/iconsumer';
import { IEvent } from '../interfaces/ievent';

// Concrete implementation for a KafkaConsumer
export class KafkaConsumer implements IConsumer {
  kafka: Kafka;
  constructor(broker: string) {
    this.kafka = new Kafka({
      brokers: [broker],
    });
  }
  async subscribe(
    topic: string,
    consumerGroup: string,
    callback: (event: IEvent) => void,
    fromBeginning = true,
  ): Promise<void> {
    const consumer = this.kafka.consumer({
      groupId: consumerGroup,
    });

    await consumer
      .connect()
      .then(() => {
        logger.info('Connected to kafka server');
      })
      .catch((error) => {
        logger.info(`error encountered while consumer connect ${error.message}`);
      });
    await consumer.subscribe({ topics: [topic], fromBeginning }).catch((error) => {
      logger.info(`error encountered while consumer subscribing ${error.message}`);
    });
    await consumer.run({
      eachBatchAutoResolve: true,
      eachMessage: async ({ message }: any) => {
        callback(JSON.parse(message));
        logger.info(`Recieved Message on Common Node :${message.value?.toString()}`);
      },
    });
  }
}
