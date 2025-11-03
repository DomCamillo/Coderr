from rest_framework import serializers
from orders.models import Order
from offers.models import OfferDetails


class OrderCreateSerializer(serializers.Serializer):
    """Serializer for creating an Order."""
    offer_detail_id = serializers.IntegerField()
    def validate_offer_detail_id(self, value):
        """Validate if the offer detail exists."""
        try:
             OfferDetails.objects.get(id=value)
        except OfferDetails.DoesNotExist:
            raise serializers.ValidationError("Offer detail does not exist.")
        return value

    def create(self, validated_data):
        """ Create Order and copy data from OfferDetail.
        Snapshots offer detail data to preserve order information even if
        the original offer is modified or deleted later.
        """
        offer_detail = OfferDetails.objects.get(id=validated_data['offer_detail_id'])
        order = Order.objects.create(
            customer_user=self.context['request'].user,
            business_user=offer_detail.offer.user,
            offer_detail=offer_detail,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
            status='in_progress'
        )
        return order


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order model."""
    class Meta:
        model = Order
        fields = ['id', 'customer_user', 'business_user', 'title', 'revisions',
                  'delivery_time_in_days', 'price', 'features', 'offer_type',
                  'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'customer_user', 'business_user', 'title',
                            'revisions', 'delivery_time_in_days', 'price',
                            'features', 'offer_type', 'created_at', 'updated_at']


class OrderCountSerializer(serializers.Serializer):
    """Serializer for counting Orders."""
    order_count = serializers.IntegerField()


class CompletedOrderCountSerializer(serializers.Serializer):
    """Serializer for counting completed Orders."""
    completed_order_count = serializers.IntegerField()
