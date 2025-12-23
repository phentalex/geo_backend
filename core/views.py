from django.contrib.gis.geos import Point as GeoPoint
from rest_framework import generics, permissions

from points.constants import SRID_GPS


class BaseGeoCreateView(generics.CreateAPIView):
    """
    Создание географической точки.

    Endpoint:
    POST /api/points/

    Использует PointSerializer для:
    - приёма latitude/longitude;
    - валидации координат;
    - сохранения location.

    Требует авторизации.
    """

    user_field = None
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Сохраняет объект, автоматически подставляя request.user
        в поле user_field.
        """
        if not self.user_field:
            raise AssertionError(
                "user_field должен быть определён в подклассе."
            )

        serializer.save(**{self.user_field: self.request.user})


class BaseGeoSearchView(generics.ListAPIView):
    """
    Базовый view для географического поиска в радиусе.

    Реализует:
    - валидацию query-параметров
    - создание GeoPoint
    - базовую структуру поиска

    Требует переопределения метода filter_queryset_by_radius().
    """

    search_serializer_class = None
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Общая логика:
        - валидирует параметры
        - создаёт GeoPoint
        - передаёт управление в дочерний класс
        """
        serializer = self.search_serializer_class(
            data=self.request.query_params
        )
        serializer.is_valid(raise_exception=True)

        lat = serializer.validated_data["latitude"]
        lon = serializer.validated_data["longitude"]
        radius = serializer.validated_data["radius"]

        center = GeoPoint(lon, lat, srid=SRID_GPS)

        return self.filter_queryset_by_radius(center, radius)

    def filter_queryset_by_radius(self, center, radius):
        """
        ДОЛЖЕН быть переопределён в наследнике.

        Параметры:
        - center: GeoPoint
        - radius: (в километрах)
        """
        raise NotImplementedError(
            "filter_queryset_by_radius() должен быть переопределён."
        )
