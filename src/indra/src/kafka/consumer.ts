import { logger } from "@cashoco/common";
import { Kafka, Consumer } from "kafkajs";
import { Topic_health } from "./topics";

export class KafkaConsumer{
    
    private consumer :Consumer
    constructor(){
        const kafka =new Kafka({
            brokers:['kafka-service:9092']
        })
        this.consumer=kafka.consumer({
            groupId: 'health_consumer_group'
            })    
    }

    public async Process_message() {
        await this.consumer.connect();            
        await this.consumer.subscribe({topics:[Topic_health] , fromBeginning:true})
        await this.consumer.run({
            eachMessage:async ( {message }) => {
                logger.info(`Recieved Message :${message.value?.toString()}`);
              },
        })
     }
    public Stop (){
        this.consumer.stop();
    }
}