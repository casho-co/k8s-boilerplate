import express from 'express';
import { morganMiddleware, logger, errorHandler, KafkaProducer } from '@cashoco/shared';
import healthRouter from './api/health';
import apiRouter from './api';

const app = express();
app.locals.kafkaProducer = KafkaProducer.getInstance(process.env.KAFKA_BROKER!);
const port = 3000;

app.use(morganMiddleware);
app.use('/health', healthRouter);
app.use('/api/indra', apiRouter);

app.use(errorHandler);

app.listen(port, () => {
  logger.info(`Server running att http://localhost:${port}`);
});
