from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import (
    RegistrationView, LoginView, EmailCheckView
)

urlpatterns = [

    # """"Login & Registration""""
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='register'),
    path('email-check/', EmailCheckView.as_view(), name='email-check'),


]
