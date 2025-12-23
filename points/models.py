from django.conf import settings
from django.contrib.gis.db import models

from .constants import SRID_GPS, TITLE_MAX_LENGHT


class Point(models.Model):
    """
    Модель географической точки на карте.

    Используется для:
    - создания точек на карте;
    - поиска точек в заданном радиусе от координат;

    Поля:
    - owner: пользователь, создавший точку;
    - title: название точки (необязательно);
    - location: географическое положение точки;
    -created_at: дата и время создания точки.
    """

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='points',
        verbose_name='Автор',
    )
    title = models.CharField(
        max_length=TITLE_MAX_LENGHT,
        verbose_name='Название точки',
    )
    location = models.PointField(
        geography=True,
        srid=SRID_GPS,
        verbose_name='Географическое положение',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создано',
    )

    class Meta:
        verbose_name = 'точка'
        verbose_name_plural = 'Точки'

    def __str__(self):
        return self.title
