from django.http import JsonResponse
from ashura._ashura import settings
import jwt

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not self.is_authenticated(request):
            return JsonResponse({'error': 'Unauthorized'}, status=401)

        response = self.get_response(request)
        return response

    def is_authenticated(self, request):    
        token = request.headers.get('Authorization')
        if token:
            user_data=self.verify_token(token)
            if user_data:
                request.user = user_data
                return True
        return False

    def verify_token(self, token):

        try:
            payload = jwt.decode(token, settings.TOKEN_KEY, algorithms=['HS256'])
            return payload
        
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            return False

