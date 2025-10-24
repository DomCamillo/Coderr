from rest_framework import serializers
from django.contrib.auth.models import User
from offers.models import Offer, OfferDetails


class OfferSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'price',
                'created_at', 'updated_at', 'min_price', 'min_delivery_time']
        read_only_fields = ['user', 'created_at', 'updated_at']

    def get_price(self, obj):
        return obj.price

    def get_min_price(self, obj):
        return obj.min_price

    def get_min_delivery_time(self, obj):
        return obj.min_delivery_time

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.min_price = validated_data.get('min_price', instance.min_price)
        instance.min_delivery_time = validated_data.get('min_delivery_time', instance.min_delivery_time)
        instance.save()
        return instance


class OfferDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetails
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days',
                  'price', 'features', 'offer_type']
        read_only_fields = ['id']


class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailsSerializer(many=True)
    user_details = serializers.SerializerMethodField(read_only=True)
    min_price = serializers.SerializerMethodField(read_only=True)
    min_delivery_time = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description',
                  'created_at', 'updated_at', 'details',
                  'min_price', 'min_delivery_time', 'user_details']

        read_only_fields = ['user', 'created_at', 'updated_at']

    def get_user_details(seld, obj):
        user = obj.user
        return {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }

    def get_min_price(self, obj):
        details = obj.details.all()
        if details.exists():
            return min(d.price for d in details)

    def get_min_delivery_time(self, obj):
        details = obj.details.all()
        if details.exists():
            return min(d.delivery_time_in_days for d in details)
        return 0

    def validate_details(self, value):
        if len(value) != 3:
            raise serializers.ValidationError("Offer needs exactly 3 details!")

        types = [d['offer_type'] for d in value]
        required_types = ['basic', 'standard', 'premium']

        if sorted(types) != sorted(required_types):
            raise serializers.ValidationError(
                "Details müssen 'basic', 'standard' und 'premium' enthalten!"
            )

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
            instance.details.all().delete()
            for detail_data in details_data:
                OfferDetails.objects.create(offer=instance, **detail_data)
        return instance


