from django.http import Http404
from rest_framework import generics
from profiles.models import Profile
from profiles.api.serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

class BusinessProfileView(generics.ListAPIView):
    queryset = Profile.objects.filter(type='business')
    serializer_class = ProfileSerializer


class CustomerProfileView(generics.ListAPIView):
    queryset = Profile.objects.filter(type='customer')
    serializer_class = ProfileSerializer


class CustomerProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.filter(type='customer')
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]


class BusinessProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.filter(type='business')
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]