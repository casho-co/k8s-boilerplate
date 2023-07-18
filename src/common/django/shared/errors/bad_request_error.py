from typing import List
from .custom_error import CustomError, IErrorStruct


class BadRequestError(CustomError):
    status_code = 400

    def __init__(self, message: str, field: str = None):
        self.message = message
        self.field = field
        super().__init__(self.message)

    def serialize_errors(self) -> List[IErrorStruct]:
        return [IErrorStruct(message=self.message, field=self.field).to_dict()]
