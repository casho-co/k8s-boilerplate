import json
import logging
import time
import uuid
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes

logger = logging.getLogger('ashura_app')

class CreateToken(APIView):
    authentication_classes=()
    def post(self, request):
        data = {"uuid":str(uuid.uuid4()),"email":"test@test.com","username":"testuser"}
        token = RefreshToken()
        token['uuid']=str(uuid.uuid4())
        token['username']="testuser"
        token['email']="test@test.com"
        access = str(token.access_token)
        refresh = str(token)
        return JsonResponse({'access':access,'refresh':refresh})

class TokenTest(APIView):
    def post(self,request):
        logger.info(request.user.username)
        return JsonResponse({'message':'Token Verified'})
    
class TokenRefresh(TokenRefreshView):
    def post(self,request):
        time.sleep(5)
        return super().post(request)