from django.urls import reverse
from django.views import generic

from rest_framework import viewsets

from .models import Place
from .serializers import PlaceSerializer


class MapPage(generic.ListView):
    model = Place
    template_name = "index.html"
    context_object_name = "places"

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
                        "coordinates": [place.lng, place.lat],
                    },
                    "properties": {
                        "title": place.title,
                        "placeId": place.id,
                        "detailsUrl": reverse(
                            "place-detail",
                            args=(place.id,),
                        ),
                    },
                }
            )

        geo_data = {"type": "FeatureCollection", "features": features}

        context["geo_data"] = geo_data
        return context


class PlaceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
