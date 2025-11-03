
from reviews.models import Review
from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from reviews.api.serializers import ReviewSerializer
from reviews.api.permissions import isReviewOwner, IsCustomer
from django.db.models import Q



class ReviewsViewSet(viewsets.ModelViewSet):
    """ Simple CURD for Reviews with dynamic costume permissions and filtering """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filter_fields=['business_user', 'reviewer']
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['updated_at', 'rating']
    ordering=['-created_at']
    pagination_class = None


    def get_queryset(self):
        return Review.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsCustomer()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), isReviewOwner()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
       serializer.save(reviewer=self.request.user)