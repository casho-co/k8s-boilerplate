import { logger } from '@cashoco/common';
import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';

export interface CustomRequest extends Request {
  user?: any ;
}

export const authenticateToken = (req: CustomRequest, res: Response, next: NextFunction) => {
  try {
    const token = req.headers.authorization!.split(' ')[1];
    const decoded = jwt.verify(token, process.env.JWT_KEY!);
    const secretdata = decoded as Record<string, any>
    req.user=(secretdata['data'])
    next();
  } 
  catch (err : any) {
    logger.error(`message: ${err.message}`)
    return res.status(401).send({ message: 'Authentication failed' });
  }
};
