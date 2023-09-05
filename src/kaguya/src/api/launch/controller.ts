import { Request, Response } from 'express';
import { logger, DatabaseConnectionError } from '@cashoco/shared';

export const ping = (req: Request, res: Response) => {
  logger.info(`request ID ${req.header('x-request-id')}`);
  const queue = req.app.locals.fetchQueue;
  queue.add('fetch_all_data', 'test');
  res.json({ message: 'kaguya V1' }).status(200);
};

export const error = (req: Request, res: Response) => {
  logger.info(`request ID ${req.header('x-request-id')}`);
  throw new DatabaseConnectionError();
};

export const verify = (req: Request, res: Response) => {
  logger.info(`user info ${req.currentUser?.user_info.email}`);
  res.json({ message: 'kaguya V1' }).status(200);
};
