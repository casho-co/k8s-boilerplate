import { Router } from 'express';
import { ping, error, verify } from './controller';
import { requireAuth } from '@cashoco/shared';

const router: Router = Router();

router.get('/ping/', ping);

router.get('/error/', error);

router.get('/verify/', requireAuth, verify);

export default router;
