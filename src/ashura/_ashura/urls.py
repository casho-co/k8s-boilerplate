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
import logging
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from requests import Response
from errors.database_connection_error import DatabaseConnectionError
from health.kafka.producer import KafkaProducer
from health.kafka.topics import TOPIC_HEALTH
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response


logger = logging.getLogger("ashura_app")


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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_token(request):

    logger.info("token valid")
    return JsonResponse({'username': request.user.username,
        'message':'successfull'})
    
@api_view(['GET'])
def create_user(request):
    user = User.objects.create_user(username='test', email='test@test.com', password='test4')
    return JsonResponse({'message':'successfull'})
urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/ashura/", message),
    path("api/ashura/error/", error),
    path("health/", include("health.urls")),
    path('api/ashura/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/ashura/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/ashura/token/test/',test_token),
    path('api/ashura/createuser/',create_user)

]
