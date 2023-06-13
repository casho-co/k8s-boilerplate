import { logger } from "@cashoco/common";
import { Kafka, Producer, ProducerRecord } from "kafkajs";

const KAFKA_BROKER :string = process.env.KAFKA_BROKER!;

export class KafkaProducer{
    
    private static instance: KafkaProducer;
    private producer: Producer;
    
    constructor()
    {
        const kafka = new Kafka({
            brokers:[KAFKA_BROKER]
        })
        this.producer=kafka.producer()      
    }

    public static getInstance(): KafkaProducer {
        if(!KafkaProducer.instance){
            KafkaProducer.instance= new KafkaProducer();
        }
        return KafkaProducer.instance;
  }
    
    public sendMessage = async ( topic:string, message: string)=>{
        await this.producer.connect()

        const payload: ProducerRecord ={
            topic,
            messages:[{value:message}],
        }
        
        await this.producer.send(payload)
            .then(()=>{
                logger.info(`Message sent to Kafka: ${message}`);
            })
            .catch(err=>{ 
                logger.error(`Error occurred while producing to Kafka: ${err}`);
            })
   }
}