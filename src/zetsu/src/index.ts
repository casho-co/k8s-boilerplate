import express, { Request, Response } from 'express';
import connectDB from './database';
import { morganMiddleware, logger, errorHandler, KafkaProducer } from '@cashoco/shared';
import apiRouter from './api';
import healthRouter from './api/health';
import './kafka/events';

const app = express();
app.locals.kafkaProducer = KafkaProducer.getInstance(process.env.KAFKA_BROKER!);
const port = 3010;

connectDB();
app.use(morganMiddleware);
app.use('/health', healthRouter);

app.use('/api/zetsu', apiRouter);

app.use(errorHandler);

app.listen(port, () => {
  logger.info(`Server running at http://localhost:${port}`);
});
