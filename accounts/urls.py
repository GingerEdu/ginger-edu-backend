from django.urls import path
from rest_framework.authtoken import views

from .views import SignUpApiView


urlpatterns = [
    path('api-token-auth', views.obtain_auth_token),
    path('sign-up', SignUpApiView.as_view()),
]
