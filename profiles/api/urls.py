from django.urls import path
from profiles.api.views import CustomerProfileView, BusinessProfileView, ProfileDetailView, delete_profile_image


urlpatterns = [
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profiles/customer/', CustomerProfileView.as_view(), name='customer-profile'),
    path('profiles/business/', BusinessProfileView.as_view(), name='business-profile'),

    path('profile/<int:pk>/delete-image/', delete_profile_image, name='delete-profile-image'),

]
