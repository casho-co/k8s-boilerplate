import { Router } from 'express';
import launch from './launch';

const router: Router = Router();

router.use('/', launch);

export default router;
