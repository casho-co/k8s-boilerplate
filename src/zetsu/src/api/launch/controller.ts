import { Request, Response } from 'express';
import { logger, DatabaseConnectionError } from '@cashoco/shared';
import { TOPIC_HEALTH } from '../../kafka/topics';

export const ping = (req: Request, res: Response) => {
  logger.info(`request ID ${req.header('x-request-id')}`);
  const producer = req.app.locals.kafkaProducer;
  const event = {
    eventType: 'test event',
    data: 'test data',
  };
  producer.sendMessage(TOPIC_HEALTH, event);
  res.json({ message: 'Indra V1' }).status(200);
};

export const error = (req: Request, res: Response) => {
  logger.info(`request ID ${req.header('x-request-id')}`);
  throw new DatabaseConnectionError();
};

export const verify = (req: Request, res: Response) => {
  logger.info(`user info ${req.currentUser?.email}`);
  res.json({ message: 'Indra V1' }).status(200);
};
