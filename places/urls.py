from django.urls import path
from django.views.generic import RedirectView

from .views import MapPage

app_name = 'places'

urlpatterns = [
    path('', RedirectView.as_view(url='map/', permanent=True)),
    path('map/', MapPage.as_view(), name='map')
]