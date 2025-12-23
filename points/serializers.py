from django.contrib.gis.geos import Point
from rest_framework import serializers

from .constants import SRID_GPS
from .models import Point as PointModel
from core.serializers import BaseGeoSearchSerializer


class PointSeriailizer(serializers.ModelSerializer):
    """
    Сериализатор гео-точек.

    Принимает:
    - latitude: широта (в градусах);
    - longitude: долгота (в градусах).

    Автоматически:
    - location: сохраняет местоположенгие как GIS Point.
    """

    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)

    class Meta:
        model = PointModel
        fields = (
            'id',
            'title',
            'latitude',
            'longitude',
            'location',
            'created_at'
        )
        read_only_fields = ('id', 'location', 'created_at')

    def validate(self, attrs):
        """Валидация входных данных географических координат."""
        lat = attrs.get('latitude')
        lon = attrs.get('longitude')

        if not (-90 <= lat <= 90):
            raise serializers.ValidationError(
                {
                    'latitude': 'Должно быть в диапазоне [-90; 90].'
                }
            )
        if not (-180 <= lon <= 180):
            raise serializers.ValidationError(
                {
                    'longitude': 'Должно быть в диапазоне [-180; 180].'
                }
            )

        return attrs

    def create(self, validated_data):
        """Создание объекта гео-точки на основе валидированных данных."""
        lat = validated_data.pop('latitude')
        lon = validated_data.pop('longitude')

        validated_data['location'] = Point(lon, lat, srid=SRID_GPS)

        return super().create(validated_data)


class PointSearchSerializer(BaseGeoSearchSerializer):
    """
    Параметры поиска гео-точек.
    """
    pass
