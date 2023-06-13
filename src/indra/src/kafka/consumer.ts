import { logger } from "@cashoco/common";
import { Kafka, Consumer } from "kafkajs";
import { Topic_health } from "./topics";
import { error, log } from "console";

export class KafkaConsumer {
    
    public async Process_message() {
        const kafka = new Kafka({
            brokers: ['kafka-service:9092']
        })
        const consumer = kafka.consumer({
            groupId: 'health_consumer_group_node'
        })
        await consumer.connect()
                        .then(()=>{
                            logger.info('Connected to kafka server')})
                        .catch(error=>{
                            logger.info(`error encountered while consumer connect ${error.message}`)
                        }); 
        await consumer.subscribe({ topics: [Topic_health], fromBeginning: true }).catch(error=>{
            logger.info(`error encountered while consumer subscribing ${error.message}`)
        })
        await consumer.run({
            eachBatchAutoResolve: true,
            eachMessage: async ({ message }: any) => {
                logger.info(`Recieved Message on Node :${message.value?.toString()}`);
            },
        })
    }
}