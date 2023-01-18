import json

from django.core import serializers
from django.http import JsonResponse
from icecream import ic

from django.views import generic
from rest_framework import viewsets

from .models import Place
from .serializers import PlaceSerializer


class MapPage(generic.ListView):
    model = Place
    template_name = 'index.html'
    context_object_name = 'places'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        places = Place.objects.all()
        features = []
        for place in places:
            features.append(
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [place.lng, place.lat]
                    },
                    "properties": {
                        "title": place.title,
                        "placeId": place.id,
                        "detailsUrl": f"/api/places/{place.id}/"
                    }
                }
            )

        geo_json = [
            {
                "type": "FeatureCollection",
                "features": features
            }
        ]

        context['geo_json'] = geo_json
        return context


class PlaceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
