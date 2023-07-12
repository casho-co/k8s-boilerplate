import express, { Request, Response } from 'express';
import {
  morganMiddleware,
  logger,
  errorHandler,
  DatabaseConnectionError,
  KafkaProducer,
  requireAuth,
} from '@launchseed/shared';
import { TOPIC_HEALTH } from './kafka/topics';

const app = express();
app.locals.kafkaProducer = KafkaProducer.getInstance(process.env.KAFKA_BROKER!);
const port = 3000;

app.use(morganMiddleware);

app.get('/api/indra/', (req: Request, res: Response) => {
  logger.info(`request ID ${req.header('x-request-id')}`);
  logger.debug('debug info');

  const producer = req.app.locals.kafkaProducer;

  const event = {
    eventType: 'test event',
    data: 'test data',
  };

  producer.sendMessage(TOPIC_HEALTH, event);

  res.send('Indra V1');
});

app.get('/api/indra/error/', (req: Request, res: Response) => {
  logger.info(`request ID ${req.header('x-request-id')}`);
  logger.error('database error');
  throw new DatabaseConnectionError();
});

app.get('/api/indra/verify/', requireAuth, (req: Request, res: Response) => {
  logger.info(`user info ${req.currentUser?.email}`);
  logger.info(`request ID ${req.header('x-request-id')}`);
  res.send('Token Verified.');
});

app.use(errorHandler);

app.listen(port, () => {
  logger.info(`Server running att http://localhost:${port}`);
});
