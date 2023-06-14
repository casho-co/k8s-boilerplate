import { logger } from '@cashoco/common';
import { Kafka } from 'kafkajs';
import { TOPIC_HEALTH } from './topics';
import { error } from 'console';

const KAFKA_BROKER: string = process.env.KAFKA_BROKER!;

async function processMessage() {
  const kafka = new Kafka({
    brokers: [KAFKA_BROKER],
  });
  const consumer = kafka.consumer({
    groupId: 'health_consumer_group_node',
  });
  await consumer
    .connect()
    .then(() => {
      logger.info('Connected to kafka server');
    })
    .catch((error) => {
      logger.info(`error encountered while consumer connect ${error.message}`);
    });
  await consumer.subscribe({ topics: [TOPIC_HEALTH], fromBeginning: true }).catch((error) => {
    logger.info(`error encountered while consumer subscribing ${error.message}`);
  });
  await consumer.run({
    eachBatchAutoResolve: true,
    eachMessage: async ({ message }: any) => {
      logger.info(`Recieved Message on Node :${message.value?.toString()}`);
    },
  });
}
processMessage().catch((error) => {
  logger.info(error);
});
