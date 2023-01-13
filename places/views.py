from django.views import generic
from rest_framework import viewsets

from .models import Place
from .serializers import PlaceSerializer


class MapPage(generic.ListView):
    model = Place
    template_name = 'index.html'
    context_object_name = 'places'


class PlaceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Place.objects.prefetch_related('img_place').all()
    serializer_class = PlaceSerializer
