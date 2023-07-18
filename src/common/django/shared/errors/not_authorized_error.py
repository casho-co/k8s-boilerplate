from typing import List
from .custom_error import CustomError, IErrorStruct


class NotAuthorizedError(CustomError):
    status_code = 401

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def serialize_errors(self) -> List[IErrorStruct]:
        return [IErrorStruct(message=self.message, field=self.field).to_dict()]
