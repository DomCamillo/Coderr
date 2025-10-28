from rest_framework import serializers
from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'business_user','reviewer','rating','description', 'created_at', 'updated_at']

        read_only_fields = ['id', 'reviewer', 'created_at', 'updated_at']

    def validate_business_user(self, value):
        if value == self.context['request'].user:
            raise serializers.ValidationError("You can not review yourself")
        return value

    def validate(self, data):
        business_user = data.get('business_user')
        if business_user and hasattr(business_user, 'profile'):
            if business_user.profile.type != 'business':
                raise serializers.ValidationError({'business_user': 'Only Business-user can get Reviewd'})
            return data