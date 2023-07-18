import { CustomError, IErrorStruct } from './custom-error';

export class ForbiddenError extends CustomError {
  statusCode = 403;

  constructor(public message: string = "Access Forbidden") {
    super(message);
    Object.setPrototypeOf(this, ForbiddenError.prototype);
  }

  serializeErrors(): IErrorStruct[] {
    return [{ message: this.message }];
  }
}
