from django.http import Http404
from rest_framework import generics
from profiles.models import Profile
from rest_framework.response import Response
from profiles.api.serializers import ProfileSerializer, ProfileListSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

class BusinessProfileView(generics.ListAPIView):
    queryset = Profile.objects.filter(type='business')
    serializer_class = ProfileListSerializer
    pagination_class = None


class CustomerProfileView(generics.ListAPIView):
    queryset = Profile.objects.filter(type='customer')
    serializer_class = ProfileListSerializer
    pagination_class = None


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_profile_image(request, pk):
    try:
        profile = Profile.objects.get(pk=pk)
        if profile.user != request.user:
            return Response({'detail': 'You only can delete your own profile image.'}, status=403)
        if profile.file:
            profile.file.delete(save=True)
            return Response({'detail':'Prfile image was succesfully deleted'},status=200)
        return Response({'detail': 'no profile image found'}, status=404)
    except Profile.DoesNotExist:
        return Response({"detail": "Profil nicht gefunden"}, status=404)
