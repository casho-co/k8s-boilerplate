import { Request, Response } from 'express';
import { logger } from '@cashoco/shared';

export const live = (req: Request, res: Response) => {
  logger.info('Checking the liveness of the application');
  res.status(200).json({ message: 'Application is live' });
};
