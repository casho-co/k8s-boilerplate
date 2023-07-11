from abc import ABC, abstractmethod
from .ievent import IEvent

class IProducer(ABC):
    @abstractmethod
    def send_message(self, topic, event: IEvent) -> None:
        pass
