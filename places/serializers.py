from abc import ABC

from rest_framework import serializers

from MoscowMap.settings import MEDIA_URL
from .models import Place


class CordSerializer(serializers.BaseSerializer, ABC):

    def to_representation(self, value):
        return {'lng': value.lng, 'lat': value.lat}


class ImageSerializer(serializers.BaseSerializer, ABC):

    def to_representation(self, value):
        return f'{MEDIA_URL}{str(value.file)}'


class PlaceSerializer(serializers.ModelSerializer):
    coordinates = CordSerializer(source='*')
    imgs = ImageSerializer(source='img_place', many=True)

    class Meta:
        model = Place
        fields = (
            'title',
            'imgs',
            'description_short',
            'description_long',
            'coordinates'
        )
