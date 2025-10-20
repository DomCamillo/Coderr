from django.urls import path, include
from rest_framework.routers import SimpleRouter
from profiles.api.views import CustomerProfileView, BusinessProfileView, CustomerProfileDetailView, BusinessProfileDetailView, ProfileDetailView


urlpatterns = [
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profile/', ProfileDetailView.as_view(), name='profile'),

    path('profiles/customer/', CustomerProfileView.as_view(), name='customer-profile'),
    path('profiles/customer/<int:pk>/', CustomerProfileDetailView.as_view(), name='customer-profile'),

    path('profiles/business/', BusinessProfileView.as_view(), name='business-profile'),
    path('profiles/business/<int:pk>/', BusinessProfileDetailView.as_view(), name='business-profile'),

]
