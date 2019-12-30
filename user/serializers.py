from rest_framework import serializers
from .models import User


class UserSerializerEmpty(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ()


class UserSerializerList(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name')


class UserSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'phone_number', 'phone_random',
                  'phone_validation', 'register_date')
