from datetime import datetime
class IEvent:
    def __init__(self, eventType: str = None, data: any = None):
        self.eventType = eventType
        self.data = data
        self.createdAt = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        
    def to_dict(self):
        return {
            'eventType': self.eventType,
            'data': self.data,
            'createdAt': self.createdAt
        }
    
    def from_dict(self, data):
        for field in ['eventType', 'data', 'createdAt']:
            if field in data:
                setattr(self, field, data[field])
        return self