from fastapi import APIRouter, Request
from shared.broker import IEvent, topics_registry
from ...kafka.config import Topics

router = APIRouter()

@router.get('/')
def ping(request: Request):
    event_object = IEvent(
            topics_registry[Topics.HEALTH.value].produce_check_health(),
            {"data": 'check check'}
        )
    request.app.kafka_producer.send_message(
        Topics.HEALTH.value,
        event_object
    )
    return {"message": "Hagoromo V1"}

