import { logger } from "@cashoco/common";
import { Kafka, Producer, ProducerRecord } from "kafkajs";

export class KafkaProducer{
    
    private static instance: KafkaProducer;
    private producer: Producer;
    
    constructor()
    {
        const kafka = new Kafka({
            brokers:['kafka-service:9092']
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
                            .then(()=>{logger.info(`Message sent to Kafka: ${message}`)})
                            .catch(err=>{ logger.error(`Error occurred while producing to Kafka: ${err}`)})
   }
}