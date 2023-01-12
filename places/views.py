from django.views import generic

from .models import Place


class MapPage(generic.ListView):
    model = Place
    template_name = 'index.html'
    context_object_name = 'places'
