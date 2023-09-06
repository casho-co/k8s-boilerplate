import { Router } from 'express';
import { live, ready } from './controller';
import { read } from 'fs';

const router: Router = Router();

router.get('/live/', live);
router.get('/ready/', ready);

export default router;
