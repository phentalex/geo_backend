from rest_framework import serializers


class BaseGeoSearchSerializer(serializers.Serializer):
    """
    Базовый сериализатор для географического поиска по радиусу.

    Используется для валидации принимаемых параметров:
    - latitude (в граудсах)
    - longitude (в граудсах)
    - radius (в километрах)
    """

    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    radius = serializers.FloatField(min_value=0)

    def validate(self, attrs):
        """
        Проверяет корректность координат и радиуса.
        """
        lat = attrs["latitude"]
        lon = attrs["longitude"]
        radius = attrs["radius"]

        if not (-90 <= lat <= 90):
            raise serializers.ValidationError(
                {"latitude": "Должно быть в диапазоне [-90; 90]."}
            )

        if not (-180 <= lon <= 180):
            raise serializers.ValidationError(
                {"longitude": "Должно быть в диапазоне [-180; 180]."}
            )

        if radius <= 0:
            raise serializers.ValidationError(
                {"radius": "Радиус должен быть больше 0."}
            )

        return attrs
