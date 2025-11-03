from rest_framework import serializers
from django.contrib.auth.models import User
from offers.models import Offer, OfferDetails


class OfferDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetails
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days',
                  'price', 'features', 'offer_type']
        read_only_fields = ['id']




class OfferDetailSerializer(serializers.ModelSerializer):
    """Serializer for GET /api/offers/{id}/ - only shows URLs of Details"""
    details = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description',
                  'created_at', 'updated_at', 'details',
                  'min_price', 'min_delivery_time']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def get_details(self, obj):
        """returns full id"""
        request = self.context.get('request')
        return [
            {
                'id': detail.id,
                'url': request.build_absolute_uri(f'/api/offerdetails/{detail.id}/')
            }
            for detail in obj.details.all()
        ]

    def get_min_price(self, obj):
        details = obj.details.all()
        return min(d.price for d in details) if details.exists() else 0

    def get_min_delivery_time(self, obj):
        details = obj.details.all()
        return min(d.delivery_time_in_days for d in details) if details.exists() else 0


class OfferSerializer(serializers.ModelSerializer):
    """Serializer for POST and PATCH - with full Details"""
    details = OfferDetailsSerializer(many=True,)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']
        read_only_fields = ['id']

    def validate_details(self, value):
        """ Ensure exactly 3 details with required types on creation.
        On update, ensure at least one detail is provided. On patch details must include 'offer_type'."""
        if self.instance is None:
            if len(value) != 3:
                raise serializers.ValidationError("Offer needs exactly 3 details!")
            types = [d['offer_type'] for d in value]
            required_types = ['basic', 'standard', 'premium']

            if sorted(types) != sorted(required_types):
                raise serializers.ValidationError( "Details must include basic, standard, and premium types!")
        else:
            if value is None or len(value) == 0:
                raise serializers.ValidationError("Details cannot be empty. Provide at least one detail to update.")
            for detail in value:
                if 'offer_type' not in detail:
                    raise serializers.ValidationError("Each detail must include 'offer_type' field.")
        return value

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        offer = Offer.objects.create(**validated_data)
        for detail_data in details_data:
            OfferDetails.objects.create(offer=offer, **detail_data)
        return offer

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)
        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        if details_data:
            for detail_data in details_data:
                offer_type = detail_data.get('offer_type')
                if offer_type:
                    detail = instance.details.filter(offer_type=offer_type).first()
                    if detail:
                        for key, value in detail_data.items():
                            setattr(detail, key, value)
                        detail.save()

        return instance



class OfferListSerializer(serializers.ModelSerializer):
    """Serializer for listing offers - includes user details and summary info"""
    user_details = serializers.SerializerMethodField()
    details = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description',
                  'created_at', 'updated_at', 'details',
                  'min_price', 'min_delivery_time', 'user_details']

    def get_details(self, obj):
        """Return list of detail IDs and URLs."""
        return [
            {
                'id': detail.id,
                'url': f'/api/offerdetails/{detail.id}/'
            }
            for detail in obj.details.all()
        ]

    def get_user_details(self, obj):
        return {
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
            'username': obj.user.username
        }

    def get_min_price(self, obj):
        """Get minimum price among offer details."""
        details = obj.details.all()
        return min(d.price for d in details) if details.exists() else 0

    def get_min_delivery_time(self, obj):
        """Get minimum delivery time among offer details."""
        details = obj.details.all()
        return min(d.delivery_time_in_days for d in details) if details.exists() else 0