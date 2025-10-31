from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Avg
from offers.models import Offer
from orders.models import Order
from profiles.models import Profile
from reviews.models import Review

class BaseInfoView(APIView):
    permission_classes = []
    def get(self, request):
        review_count = Review.objects.count()
        average_rating = Review.objects.aggregate(avg=Avg('rating'))['avg']
        average_rating = round(average_rating, 2) if average_rating is not None else None
        business_profile_count = Profile.objects.filter(type='business').count()
        offer_count = Offer.objects.count()


        data = {
            "review_count" : review_count,
            "average_rating": average_rating,
            "business_profile_count": business_profile_count,
            "offer_count": offer_count,
        }
        return Response(data)

