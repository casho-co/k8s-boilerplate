from datetime import datetime
class IEvent:
    def __init__(self, eventType: str, data: any):
        self.eventType = eventType
        self.data = data
        self.createdAt = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        
    def __dict__(self):
        return {
            'eventType': self.eventType,
            'data': self.data,
            'createdAt': self.createdAt
        }