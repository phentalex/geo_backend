from rest_framework import serializers

from .models import Message
from core.serializers import BaseGeoSearchSerializer
from points.models import Point


class MessageSerializer(serializers.ModelSerializer):
    """
    Сериализатор сообщения, привязанного к гео-точке.

    Принимает:
    - point_id: id точки, к которой относится сообщение;
    - text: текст сообщения.

    Автоматически:
    - author: подставляет автора из request.user.
    """

    point_id = serializers.PrimaryKeyRelatedField(
        source='point',
        queryset=Point.objects.all(),
        write_only=True,
    )

    class Meta:
        model = Message
        fields = (
            'id',
            'point_id',
            'text',
            'author',
            'created_at',
        )
        read_only_fields = ('id', 'author', 'created_at')

    def create(self, validated_data):
        """Создание сообщения и привязка автора из текущего запроса."""
        request = self.context.get('request')
        validated_data['author'] = request.user
        return super().create(validated_data)


class MessageSearchSerializer(BaseGeoSearchSerializer):
    """
    Параметры поиска сообщений по географии.
    """
    pass
