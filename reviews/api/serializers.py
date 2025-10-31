from rest_framework import serializers
from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'business_user','reviewer','rating','description', 'created_at', 'updated_at']

        read_only_fields = ['id', 'reviewer', 'created_at', 'updated_at']

    def validate(self, data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            business_user = data.get('business_user')

            if Review.objects.filter(
                reviewer=request.user,
                business_user=business_user
            ).exists():
                raise serializers.ValidationError( "You have already reviewed this business user.")
        return data

    def validate_business_user(self, value):
        if hasattr(value, 'type') and value.type != 'business':
            raise serializers.ValidationError("You can only review business users.")
        return value