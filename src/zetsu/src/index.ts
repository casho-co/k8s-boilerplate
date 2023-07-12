import express, { Request, Response } from 'express';
import connectDB from './database';
import { healthRouter } from './routes/api/health';
import { morganMiddleware, logger, errorHandler, DatabaseConnectionError, KafkaProducer } from '@launchseed/shared';
import { TOPIC_HEALTH } from './kafka/topics';

const app = express();
app.locals.kafkaProducer = KafkaProducer.getInstance(process.env.KAFKA_BROKER!);
const port = 3010;

connectDB();
app.use(morganMiddleware);
app.use('/health', healthRouter);

app.get('/api/zetsu/', (req: Request, res: Response) => {
  logger.info(`request ID ${req.header('x-request-id')}`);
  logger.debug('debug info');
  const producer = req.app.locals.kafkaProducer;
  const event = {
    eventType: 'test event',
    data: 'test data',
  };

  producer.sendMessage(TOPIC_HEALTH, event);
  res.send('Zetsu V1');
});

app.get('/api/zetsu/error/', (req: Request, res: Response) => {
  logger.info(`request ID ${req.header('x-request-id')}`);
  logger.error('database error');
  throw new DatabaseConnectionError();
});

app.use(errorHandler);

app.listen(port, () => {
  logger.info(`Server running at http://localhost:${port}`);
});
