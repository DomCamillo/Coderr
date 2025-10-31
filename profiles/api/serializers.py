from rest_framework import serializers
from django.contrib.auth.models import User
from profiles.models import Profile
from rest_framework.permissions import IsAuthenticated

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username',read_only=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
    class Meta:
        model = Profile
        fields = ['user', 'username', 'first_name', 'last_name', 'file',
                  'location', 'tel', 'description', 'working_hours', 'type', 'email','created_at']

        read_only_fields = ['type', 'user', 'created_at']

    def to_representation(self, instance):
        """"to ensure that certain fields are never null in the output"""
        data = super().to_representation(instance)

        empty_string_fields = ['first_name', 'last_name', 'location', 'tel', 'description', 'working_hours']

        for field in empty_string_fields:
            if data.get(field) is None:
                data[field] = ''

        return data

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user

        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.email = user_data.get('email', user.email)
        user.save()

        if 'file' in validated_data and validated_data['file'] is None:
            if instance.file:
                instance.file.delete(save=False)

        return super().update(instance, validated_data)


class ProfileListSerializer(serializers.ModelSerializer):
    """"""
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'username', 'first_name', 'last_name', 'file',
                  'location', 'tel', 'description', 'working_hours', 'type']

    def to_representation(self, instance):
        data = super().to_representation(instance)

        empty_string_fields = ['first_name', 'last_name', 'location',
                               'tel', 'description', 'working_hours']

        for field in empty_string_fields:
            if data.get(field) is None:
                data[field] = ''

        return data