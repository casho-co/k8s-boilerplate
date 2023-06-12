import { logger } from "@cashoco/common";
import { KafkaConsumer } from "../../kafka/consumer";

async function  StartKafkaConsumer(){
    const consumer = new KafkaConsumer()
    try{
        consumer.Process_message();
    }
    catch (error){
        console.log(error)
        logger.info(error)
    }finally{
        consumer.Stop()
    }
}
