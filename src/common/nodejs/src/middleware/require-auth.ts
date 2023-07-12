import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { logger } from '../lib/logger';
import { NotValidError, NotAuthorizedError } from '../errors';

interface UserPayload {
  uuid: string;
  username: string;
  email: string;
}

declare global {
  namespace Express {
    interface Request {
      currentUser?: UserPayload;
    }
  }
}

export const requireAuth = (req: Request, res: Response, next: NextFunction) => {
  if (!req.headers?.authorization) {
    throw new NotAuthorizedError();
  }

  try {
    const token = req.headers.authorization!.split(' ')[1];
    req.currentUser = jwt.verify(token, process.env.JWT_KEY!) as UserPayload;
  } catch (err) {
    logger.error(`message: ${err}`);
    throw new NotValidError();
  }

  next();
};
