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
import json
import logging
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from .auth import TokenAuthenticationMiddleware
from errors.database_connection_error import DatabaseConnectionError
from health.kafka.producer import KafkaProducer
from health.kafka.topics import TOPIC_HEALTH
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

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
    
@TokenAuthenticationMiddleware
def token_test(request):
    logger.info(request.user)
    return JsonResponse({'message':'Token Verified'})

@api_view(['POST'])
def create_user(request):
    payload = json.loads(request.body)
    username = payload.get('username')
    password = payload.get('password')
    user = User.objects.create_user(username=username, email='test@test.com', password=password)
    return JsonResponse({'message':'successfull'},)

def create_user_token(request):
    if request.method=='POST':
        payload = json.loads(request.body)
        username = payload.get('username')
        password = payload.get('password')
        try:
            user = User.objects.get(username=username)
            if user:
                if user.check_password(password):
                    refresh = RefreshToken.for_user(user)
                    return JsonResponse({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    },status=200)
                else:
                    return JsonResponse({'error':'Wrong Password'},status=400)
        except:
            return JsonResponse({'error':'No such user found! please signup'},status=400)
    else:
        return JsonResponse({'error':'bad method','message':'Use POST method'},status=400)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/ashura/", message),
    path("api/ashura/error/", error),
    path("health/", include("health.urls")),
    # path('api/ashura/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/ashura/token/', create_user_token),
    path('api/ashura/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/ashura/createuser/', create_user),
    path('api/ashura/test/', token_test),

]
