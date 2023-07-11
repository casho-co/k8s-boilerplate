import time
class IEvent:
    def __init__(self, eventType: str, data: any):
        self.eventType = eventType
        self.data = data
        self.createdAt = int(round(time.time() * 1000))
        
    def __dict__(self):
        return {
            'eventType': self.eventType,
            'data': self.data,
            'createdAt': self.createdAt
        }