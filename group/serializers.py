from rest_framework import serializers
from .models import Group


class GroupSerializerEmpty(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ()
