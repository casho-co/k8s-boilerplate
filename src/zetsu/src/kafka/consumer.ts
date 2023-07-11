import { KafkaConsumer, logger } from "@cashoco/common";
import { TOPIC_HEALTH } from "./topics";


const KAFKA_BROKER: string = process.env.KAFKA_BROKER!;

const consumer = new KafkaConsumer(KAFKA_BROKER)

const callback: (event)=> void = (event) => {
  logger.info(`Consumed event eventType:${event.eventType} , data: ${event.data}, created at:${event.createdAt}` )
}

consumer.subscribe(TOPIC_HEALTH, 'health_consumer_group_node',callback,true )
