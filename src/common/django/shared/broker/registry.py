topics_registry = {}

def register_topic(param):
    def decorator(cls):
        topics_registry[param] = cls
        return cls
    return decorator