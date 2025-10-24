from django.urls import path, include
from offers.api.views import OfferViewSet, OfferDetailViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'offers', OfferViewSet, basename='offer')
router.register(r'offerdetails', OfferDetailViewSet, basename='offerdetail')

urlpatterns = [
    path('', include(router.urls)),
]
