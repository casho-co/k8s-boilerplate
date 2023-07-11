import { KafkaConsumer, logger, IEvent } from '@launchseed/shared';
import { TOPIC_HEALTH } from './topics';

const KAFKA_BROKER: string = process.env.KAFKA_BROKER!;

const consumer = new KafkaConsumer(KAFKA_BROKER);

const callback = (topic: string, message: IEvent) => {
  logger.info(`Consumed event eventType:${message.eventType} , data: ${message.data}, created at:${message.createdAt}`);
};

consumer.subscribe(TOPIC_HEALTH, 'health_consumer_group_node', callback, false);
