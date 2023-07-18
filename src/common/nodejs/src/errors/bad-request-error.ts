import { CustomError, IErrorStruct } from './custom-error';

export class BadRequestError extends CustomError {
  statusCode = 400;

  constructor(public message: string = 'Bad Request', public field: string = 'None') {
    super(message);
    Object.setPrototypeOf(this, BadRequestError.prototype);
  }

  serializeErrors(): IErrorStruct[] {
    return [{ message: this.message, field: this.field }];
  }
}
