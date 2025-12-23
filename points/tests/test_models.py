import pytest
from django.contrib.gis.geos import Point as GeoPoint
from django.utils import timezone

from points.constants import SRID_GPS
from points.models import Point


pytestmark = pytest.mark.django_db


class TestPointModels:
    """Тесты моделей гео-точек."""

    @pytest.mark.parametrize(
            'lat, lon, title',
            ((37.62, 55.72, 'X'),)
    )
    def test_point_can_be_created(self, make_point, lat, lon, title, user):
        """Точка создаётся, привязывается к владельцу."""
        Point.objects.all().delete()
        point = make_point(
            longitude=lon,
            latitude=lat,
            title=title
        )
        assert Point.objects.count() == 1
        assert point.title == title
        assert point.owner == user
        assert point.location == GeoPoint(lon, lat, srid=SRID_GPS)

    def test_point_created_at_is_set_automatically(
        self,
        make_point,
    ):
        """Поле created_at добавляется автоматически при создании точки."""
        before = timezone.now()
        point = make_point()
        after = timezone.now()
        assert point.created_at is not None
        assert before <= point.created_at <= after

    @pytest.mark.parametrize(
            'lon, lat, title',
            ((45.45, 55.55, 'X'),)
    )
    def test_point_has_expected_coordinates(
            self,
            make_point,
            lat,
            lon,
            title
    ):
        """
        Проверка корректности координат через x, y:

        - x = longitude;
        - y = latitude.
        """
        Point.objects.all().delete()
        point = make_point(
            longitude=lon,
            latitude=lat,
            title=title
        )
        assert Point.objects.count() == 1
        assert point.location.x == lon
        assert point.location.y == lat
