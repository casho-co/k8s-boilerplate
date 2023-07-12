import { Router } from 'express';
import { live } from './controller';

const router: Router = Router();

router.get('/live/', live);

export default router;
