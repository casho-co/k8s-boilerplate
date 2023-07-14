import { Request, Response } from 'express';
import { logger, DatabaseConnectionError, topicsRegistry } from '@cashoco/shared';
import TOPICS from '../../kafka/config';

export const ping = (req: Request, res: Response) => {
  logger.info(`request ID ${req.header('x-request-id')}`);
  const producer = req.app.locals.kafkaProducer;
  const event = {
    eventType: topicsRegistry[TOPICS.HEALTH].produce_check_health(),
    data: 'check check',
  };
  producer.sendMessage(TOPICS.HEALTH, event);
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
