import json
from abc import ABC, abstractmethod
from typing import List, Optional


class IErrorStruct:
    def __init__(self, message: str, field: Optional[str] = None):
        self.message = message
        self.field = field
    
    def to_dict(self):
        return {
            'message': self.message,
            'field': self.field,
        }



class CustomError(Exception, ABC):
    def __init__(self, message: str):
        super().__init__(message)

    @property
    @abstractmethod
    def status_code(self) -> int:
        pass

    @abstractmethod
    def serialize_errors(self) -> List[IErrorStruct]:
        pass
