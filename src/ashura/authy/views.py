import json
import logging
import time
from django.http import JsonResponse
from django.views import View
from .middleware import TokenAuthenticationMiddleware
from django.utils.decorators import method_decorator
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

logger = logging.getLogger('ashura_app')

class create_token(View):
    def post(self, request):
        data = json.loads(request.body)
        token = RefreshToken() 
        token['data'] = data  
        access = str(token.access_token)
        refresh = str(token)
        return JsonResponse({'access':access,'refresh':refresh})

@method_decorator(TokenAuthenticationMiddleware , name='dispatch')        
class token_test(View):
    def post(self,request):
        logger.info(request.user)
        return JsonResponse({'message':'Token Verified'})
    
class refresh_token(TokenRefreshView):
    def post(self,request):
        time.sleep(5)
        return super().post(request)