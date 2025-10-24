from django.http import Http404
from rest_framework import generics
from rest_framework import status, viewsets
from rest_framework.response import Response
from offers.models import Offer, OfferDetails
from offers.api.serializers import OfferSerializer, OfferDetailsSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly , IsAuthenticated


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OfferDetailViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OfferDetails.objects.all()
    serializer_class = OfferDetailsSerializer
    permission_classes = [IsAuthenticated]