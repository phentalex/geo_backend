from django.contrib.gis.measure import D

from .models import Message
from .serializers import MessageSearchSerializer, MessageSerializer
from core.views import BaseGeoCreateView, BaseGeoSearchView


class MessageCreateView(BaseGeoCreateView):
    """
    Создание сообщения к гео-точке.

    Endpoint:
    POST /api/points/messages/
    """

    serializer_class = MessageSerializer
    user_field = "author"


class MessageSearchView(BaseGeoSearchView):
    """
    Поиск сообщений, привязанных к точкам в заданном радиусе.

    GET /api/points/messages/search/
    """

    serializer_class = MessageSerializer
    search_serializer_class = MessageSearchSerializer

    def filter_queryset_by_radius(self, center, radius):
        return Message.objects.filter(
            point__location__distance_lte=(center, D(km=radius))
        )
