import { logger } from '@cashoco/common';
import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';

export const authenticateToken = (req: Request, res: Response, next: NextFunction) => {
  try {
    const token = req.headers.authorization!.split(' ')[1];
    jwt.verify(token, process.env.JWT_KEY!,(error, decodedtoken)=>{  
      req.user = decodedtoken;
    next();
    });
  }
  catch (err: any) {
    logger.error(`message: ${err.message}`);
    return res.status(401).send({ message: 'Authentication failed' });
  }
};
