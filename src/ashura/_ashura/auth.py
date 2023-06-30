import logging
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework_simplejwt.exceptions import TokenError

logger = logging.getLogger("ashura_app")

class TokenAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.headers.get('Authorization').split(' ')[1]

        if token:
            try:
                decoded_token = AccessToken(token,verify=True)
                user_id = decoded_token['user_id']
                logger.info(user_id)
                user = User.objects.get(id=user_id)
                request.user = user
            except (TokenError, User.DoesNotExist):
                return HttpResponse('Unauthorized', status=401)

        response = self.get_response(request)
        return response