from django.urls import path, include
from core.api.views import BaseInfoView

urlpatterns = [
    path('base-info/', BaseInfoView.as_view(), name='base-info'),
]
