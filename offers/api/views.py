from django_filters import rest_framework as filters
from rest_framework import filters as drf_filters
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from orders.api.permissions import IsBusinessUser
from offers.models import Offer, OfferDetails
from offers.api.serializers import OfferSerializer, OfferDetailsSerializer, OfferListSerializer ,OfferDetailSerializer
from offers.api.permissions import IsOfferOwner
from rest_framework.permissions import IsAuthenticatedOrReadOnly , IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination


class OfferPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = OfferPagination
    filter_backends = [filters.DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]
    filterset_fields = {'user': ['exact']}
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']
    ordering = ['-updated_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return OfferListSerializer
        elif self.action == 'retrieve':
            return OfferDetailSerializer
        else:
            return OfferSerializer
    def get_queryset(self):
        queryset = Offer.objects.all()

        min_price = self.request.query_params.get('min_price')
        if min_price:
            try:
                min_price = float(min_price)
                if min_price < 0:
                    raise ValueError("Must be positive")
                queryset = queryset.filter(details__price__gte=min_price).distinct()
            except (ValueError, TypeError):
                raise ValidationError({
                    "min_price": "Must be a valid positive number"
                })

        max_delivery_time = self.request.query_params.get('max_delivery_time')
        if max_delivery_time:
            try:
                max_delivery_time = int(max_delivery_time)
                if max_delivery_time < 0:
                    raise ValueError("Must be positive")
                queryset = queryset.filter(
                    details__delivery_time_in_days__lte=max_delivery_time
                ).distinct()
            except (ValueError, TypeError):
                raise ValidationError({
                    "max_delivery_time": "Must be a valid positive integer"
                })

        return queryset

    def get_permissions(self):
        """Dynamic Permissions for different actions"""
        if self.action == 'list':
            return []
        elif self.action == 'create':
            return [IsAuthenticated(), IsBusinessUser()]
        elif self.action == 'retrieve':
            return [IsAuthenticated()]
        elif self.action in ['update','partial_update', 'destroy']:
            return [IsAuthenticated(), IsOfferOwner()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
class OfferDetailViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OfferDetails.objects.all()
    serializer_class = OfferDetailsSerializer
    permission_classes = [IsAuthenticated]