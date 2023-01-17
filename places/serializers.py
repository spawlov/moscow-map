from abc import ABC

from rest_framework import serializers

from .models import Place


class CordSerializer(serializers.BaseSerializer, ABC):
    """Serializer coordinates for to places"""
    def to_representation(self, value):
        return {'lng': value.lng, 'lat': value.lat}


class ImageSerializer(serializers.BaseSerializer, ABC):
    """Serializer list of images for to places"""
    def to_representation(self, value):
        return f'{str(value.file.url)}'


class PlaceSerializer(serializers.ModelSerializer):
    coordinates = CordSerializer(source='*')
    imgs = ImageSerializer(source='img_places', many=True)

    class Meta:
        model = Place
        fields = (
            'title',
            'imgs',
            'description_short',
            'description_long',
            'coordinates'
        )
