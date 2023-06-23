import { Request, Response, NextFunction } from 'express';
import jwt, { JwtPayload } from 'jsonwebtoken';

interface CustomRequest extends Request {
  userData?: JwtPayload;
}
export const authenticateToken = (req: CustomRequest, res: Response, next: NextFunction): void => {
  try {
    const token: string | undefined = req.headers.authorization?.split(' ')[1];
    if (!token) {
      return res.status(401).send({ message: 'Authentication failed' });
    }

    const decoded: JwtPayload | undefined = jwt.verify(token, process.env.JWT_KEY) as JwtPayload;

    if (!decoded) {
      return res.status(401).send({ message: 'Authentication failed' });
    }

    req.userData = decoded;
    next();
  } catch (err) {
    return res.status(401).send({ message: 'Authentication failed' });
  }
};

