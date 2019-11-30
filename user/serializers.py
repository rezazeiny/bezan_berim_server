from rest_framework import serializers
from .models import User


class UserSerializerEmpty(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ()
