import { Kafka } from 'kafkajs';
import { logger } from '../../lib/logger';
import { IConsumer } from '../interfaces/iconsumer';
import { topicsRegistry } from '../registry';
import { IEvent } from '../interfaces/ievent';

// Concrete implementation for a KafkaConsumer
export class KafkaConsumer implements IConsumer {
  kafka: Kafka;
  constructor(broker: string) {
    this.kafka = new Kafka({
      brokers: [broker],
    });
  }
  async subscribe(topics: string[], consumerGroup: string, fromBeginning = true): Promise<void> {
    const consumer = this.kafka.consumer({
      groupId: consumerGroup,
    });

    await consumer.connect();

    await consumer.subscribe({ topics: topics, fromBeginning }).catch((error) => {
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
        const eventMessage = JSON.parse(message.value!.toString()) as IEvent;
        logger.info(
          `Message received: 
          topic: ${topic}, 
          event : ${eventMessage.eventType}, 
          data: ${eventMessage.data}
          createdAt: ${eventMessage.createdAt}`,
        );
        if (topic in topicsRegistry) {
          const eventClass = topicsRegistry[topic];
          const functionName = `consume_${eventMessage.eventType}`;
          if (typeof eventClass[functionName] === 'function') {
            eventClass[functionName](eventMessage);
          } else {
            logger.info(`Event type ${eventMessage.eventType} is not handled by this consumer`);
          }
        } else {
          logger.info(`Topic ${topic} is not handled by this consumer`);
        }
      },
    });
  }
}
