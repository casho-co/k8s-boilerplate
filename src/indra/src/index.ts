import express, { Request, Response } from 'express';
import { morganMiddleware, logger, errorHandler, DatabaseConnectionError } from '@cashoco/common';
import { KafkaProducer } from './kafka/producer';
import { TOPIC_HEALTH } from "./kafka/topics";

const app = express();
const port = 3000;

app.use(morganMiddleware);

app.get('/api/indra/', (req: Request, res: Response) => {
  logger.info(`request ID ${req.header('x-request-id')}`);
  logger.debug('debug info');
  const producer = KafkaProducer.getInstance();
  producer.sendMessage(TOPIC_HEALTH, JSON.stringify({ eventType: 'NodeEvent' }))
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


