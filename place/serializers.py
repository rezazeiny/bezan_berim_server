from rest_framework import serializers
from .models import Place


class PlaceSerializerEmpty(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ()
