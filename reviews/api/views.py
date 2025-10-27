from rest_framework import generics
from reviews.models import Review
from rest_framework import status, viewsets
from rest_framework.response import Response
from reviews.api.serializers import ReviewSerializer
from orders.api.permissions import IsCustomer, IsOrderBusinessUser
from django.db.models import Q


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsCustomer | IsOrderBusinessUser]