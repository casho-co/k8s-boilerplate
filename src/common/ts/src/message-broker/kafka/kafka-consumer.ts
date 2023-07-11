import { Kafka } from 'kafkajs';
import { logger } from '../../lib/logger';
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
    callback: (topic: string, event: IEvent) => void,
    fromBeginning = true,
  ): Promise<void> {
    const consumer = this.kafka.consumer({
      groupId: consumerGroup,
    });

    await consumer.connect();

    await consumer.subscribe({ topics: [topic], fromBeginning }).catch((error) => {
      logger.info(`error encountered while consumer subscribing ${error.message}`);
    });

    await consumer.run({
      eachBatchAutoResolve: true,
      eachMessage: async ({ topic, partition, message, heartbeat, pause }) => {
        // console.log('message', message);
        // console.log({
        //   topic: topic,
        //   key: message.key?.toString(),
        //   value: message.value?.toString(),
        //   headers: message?.headers,
        // });
        callback(topic, JSON.parse(message.value!.toString()));
      },
    });
  }
}
