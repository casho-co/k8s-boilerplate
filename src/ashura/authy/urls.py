from django.urls import path
from . import views

urlpatterns = [
    path("token/", views.CreateToken.as_view(), name="create_token"),
    path("refresh/", views.TokenRefresh.as_view(), name='token_refresh'),
    path("verify/", views.TokenVerify.as_view(), name="index"),
]