import { CustomError } from './custom-error';

export class NotValidError extends CustomError {
  statusCode = 401;

  constructor(public reason: string = 'Token InValid') {
    super(reason);

    Object.setPrototypeOf(this, NotValidError.prototype);
  }

  serializeErrors() {
    return [{ message: this.reason }];
  }
}
