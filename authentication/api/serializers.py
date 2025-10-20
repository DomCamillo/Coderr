from rest_framework import serializers

from django.contrib.auth import get_user_model
User = get_user_model()



class RegistrationSerializer(serializers.ModelSerializer):
    """ Handles user registration."""
    repeated_password = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(choices=['customer', 'business'], write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'type']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    """  Ensure email is unique"""
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    """ Ensure both passwords match"""
    def validate(self, data):
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError(
                {'password': 'Passwords do not match'})
        return data

    def create(self, validated_data):
        from profiles.models import Profile
        user_type = validated_data.pop('type')
        validated_data.pop('repeated_password')

        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()


        Profile.objects.create(user=user, type=user_type)
        return user