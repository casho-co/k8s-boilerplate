import express, { Request, Response } from 'express';
import { morganMiddleware, logger, errorHandler, DatabaseConnectionError, KafkaProducer } from '@cashoco/common';
import { TOPIC_HEALTH } from './kafka/topics';

const app = express();
app.locals.kafkaProducer = KafkaProducer.getInstance(process.env.KAFKA_BROKER!);
const port = 3000;

app.use(morganMiddleware);

app.get('/api/indra/', (req: Request, res: Response) => {
  logger.info(`request ID ${req.header('x-request-id')}`);
  logger.debug('debug info');


  const producer = req.app.locals.kafkaProducer;
  const now = new Date().toISOString();
  const event = {
    eventType: 'test event',
    data: 'test data',
    createdAt: now,
  };
  
  producer.sendMessage(TOPIC_HEALTH, event);

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
