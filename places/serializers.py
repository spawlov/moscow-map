from abc import ABC

from rest_framework import serializers

from .models import Place


class CordSerializer(serializers.BaseSerializer, ABC):
    """Serializer coordinates for to places for coordinates variable"""
    def to_representation(self, place):
        return {'lng': place.lng, 'lat': place.lat}


class ImageSerializer(serializers.BaseSerializer, ABC):
    """Serializer list of images for to places for imgs variable"""
    def to_representation(self, image):
        return f'{image.file.url}'


class PlaceSerializer(serializers.ModelSerializer):
    coordinates = CordSerializer(source='*')  # Cords place
    imgs = ImageSerializer(source='images', many=True)  # Image list

    class Meta:
        model = Place
        fields = (
            'title',
            'imgs',
            'description_short',
            'description_long',
            'coordinates'
        )
