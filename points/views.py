from django.contrib.gis.measure import D
from rest_framework import generics, permissions

from .models import Point
from .serializers import PointSearchSerializer, PointSeriailizer
from core.views import BaseGeoCreateView, BaseGeoSearchView


class PointCreateView(BaseGeoCreateView):
    """
    Создание географической точки.

    Endpoint:
    POST /api/points/
    """

    serializer_class = PointSeriailizer
    user_field = "owner"


class PointSearchView(BaseGeoSearchView):
    """
    Поиск гео-точек в заданном радиусе.

    Endpoint:
    GET /api/points/search/
    """

    serializer_class = PointSeriailizer
    search_serializer_class = PointSearchSerializer

    def filter_queryset_by_radius(self, center, radius):
        return Point.objects.filter(
            location__distance_lte=(center, D(km=radius))
        )
