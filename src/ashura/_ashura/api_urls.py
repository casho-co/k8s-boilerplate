import logging
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from shared.broker.interfaces import IEvent
from shared.errors import DatabaseConnectionError
from rest_framework.decorators import permission_classes


logger = logging.getLogger("ashura_app")


@permission_classes([])
def message(request):
    logger.info("Request ID {0}".format(request.headers['X-Request-Id']))
    logger.info("Message view requested.")
    event_object = IEvent('test event', 'test data')
    settings.KAFKA_PRODUCER_INSTANCE.send_message(
        settings.TOPIC_HEALTH,
        event_object 
    )
    return JsonResponse({"message": "Ashura V1"}, status=200)

@permission_classes([])
def error(request):
    logger.info("Request ID {0}".format(request.headers['X-Request-Id']))
    logger.error("Error view requested.")
    raise DatabaseConnectionError()
    

urlpatterns = [
    path("ping/", message),
    path("error/", error),
    path("auth/", include("authy.urls")),
]
