import { Router, Request, Response } from 'express';
import { logger } from '@cashoco/common';

const router: Router = Router();

router.get('/live/', (req: Request, res: Response) => {
  logger.info('Checking the liveness of the application');
  res.status(200).json({ message: 'Application is live' });
});

export { router as healthRouter };
