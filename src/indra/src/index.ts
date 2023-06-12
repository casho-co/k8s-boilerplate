import express, { Request, Response } from 'express';
import { morganMiddleware, logger, errorHandler, DatabaseConnectionError } from '@cashoco/common';
import { KafkaProducer } from './kafka/producer';
import { fork } from 'child_process';
import { Topic_health } from './kafka/topics';
import { KafkaConsumer } from './kafka/consumer';

const app = express();
const port = 3000;
const KafkaConsumerStart = fork('./management/commands/kafkaconsumer.ts')

app.use(morganMiddleware);

app.get('/api/indra/', (req: Request, res: Response) => {
  logger.info(`request ID ${req.header('x-request-id')}`);
  logger.debug('debug info');
  const producer = KafkaProducer.getInstance();
  producer.sendMessage(Topic_health,'New Kafka Message')
  res.send('Indra V1');
});

app.get('/api/indra/error/', (req: Request, res: Response) => {
  logger.info(`request ID ${req.header('x-request-id')}`);
  logger.error('database error');
  throw new DatabaseConnectionError();
});

app.use(errorHandler);

app.listen(port, () => {
  logger.info(`Server running att http://localhost:${port}`);
});

const consumer = new KafkaConsumer()
try{
    consumer.Process_message().catch(e => console.error(e.message, e));
}
catch (error){
    console.log(error)
    logger.info(error)
}finally{
    consumer.Stop()
}
