from abc import ABC

from rest_framework import serializers

from .models import Place


class CordSerializer(serializers.BaseSerializer, ABC):
    """Serializer coordinates for to places for coordinates variable"""
    def to_representation(self, value):
        return {'lng': value.lng, 'lat': value.lat}


class ImageSerializer(serializers.BaseSerializer, ABC):
    """Serializer list of images for to places for imgs variable"""
    def to_representation(self, value):
        return f'{str(value.file.url)}'


class PlaceSerializer(serializers.ModelSerializer):
    coordinates = CordSerializer(source='*')  # Cords place
    imgs = ImageSerializer(source='img_places', many=True)  # Image list

    class Meta:
        model = Place
        fields = (
            'title',
            'imgs',
            'description_short',
            'description_long',
            'coordinates'
        )
