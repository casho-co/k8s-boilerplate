import { logger } from "@cashoco/common";
import { Kafka, Consumer } from "kafkajs";
import { Topic_health } from "./topics";

export class KafkaConsumer {

    constructor() {

    }

    public async Process_message() {
        const kafka = new Kafka({
            brokers: ['kafka-service:9092']
        })
        const consumer = kafka.consumer({
            groupId: 'health_consumer_group_node'
        })
        await consumer.connect();
        await consumer.subscribe({ topics: [Topic_health], fromBeginning: true })
        await consumer.run({
            eachMessage: async ({ message }: any) => {
                logger.info(`Recieved Message on Node :${message.value?.toString()}`);
            },
        })
    }
}