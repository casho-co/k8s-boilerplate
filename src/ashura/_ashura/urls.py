"""_ashura URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import datetime
import json
import logging
import jwt
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from errors.database_connection_error import DatabaseConnectionError
from health.kafka.producer import KafkaProducer
from health.kafka.topics import TOPIC_HEALTH
from ...common.py.auth.authentication_middleware import AuthenticationMiddleware

logger = logging.getLogger("ashura_app")

@AuthenticationMiddleware
def message(request):

    logger.info("Request ID {0}".format(request.headers['X-Request-Id']))
    logger.info("Message view requested.")
    producer = KafkaProducer()
    producer.send_message(TOPIC_HEALTH, {"message": "kafka message"})

    return JsonResponse({"message": "Ashura V1"}, status=200)


def error(request):
    logger.info("Request ID {0}".format(request.headers['X-Request-Id']))
    logger.error("Error view requested.")
    raise DatabaseConnectionError()

def get_token(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        username= json_data['username']

        if username :
            access_token_payload = {
            'username':username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=settings.JWT_EXPIRATION_HOURS),
            }
            access_token = jwt.encode(access_token_payload, settings.TOKEN_KEY, algorithm='HS256')

            refresh_token_payload={
            'username':username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=settings.JWT_EXPIRATION_DAYS),
                
            }
            refersh_token = jwt.encode(refresh_token_payload,settings.TOKEN_KEY,algorithm='HS256')
            return JsonResponse({
                "access_token": access_token ,
                "refresh_token": refersh_token}, status=200)

        else:
            return JsonResponse({'error':'user data should be passed in request body as json'},status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/ashura/", message),
    path("api/ashura/error/", error),
    path("health/", include("health.urls")),
    path("api/ashura/token",get_token),
    # path("api/ashura/token/refresh",),

]
