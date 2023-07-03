from django.urls import path

from . import views

urlpatterns = [
    path("token/", views.create_token.as_view(), name="create_token"),
    path("refresh/", views.refresh_token.as_view(), name='token_refresh'),
    path("test/", views.token_test.as_view(), name="index"),
]