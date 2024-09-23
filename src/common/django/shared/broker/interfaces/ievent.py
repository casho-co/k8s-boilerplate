from datetime import datetime


class IEvent:
    def __init__(self, event_type: str = None, data: any = None):
        self.event_type = event_type
        self.data = data
        self.created_at = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

    def to_dict(self):
        return {
            'event_type': self.event_type,
            'data': self.data,
            'created_at': self.created_at
        }

    def from_dict(self, data):
        for field in ['event_type', 'data', 'created_at']:
            if field in data:
                setattr(self, field, data[field])
        return self
