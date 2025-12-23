from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Message(models.Model):
    """
    Сообщение пользователя, привязанное к географической точке.

    Используется для:
    - создания сообщений, привязанных к точке;
    - поиска сообщений в заданном радиусе.

    Поля:
    - point: точка, к которой привязано сообщение;
    - author: пользователь, написавший сообщение;
    - text: текст сообщения;
    - created_at: дата и время создания сообщения.
    """

    point = models.ForeignKey(
        'points.Point',
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Точка',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Автор',
    )
    text = models.TextField(
        verbose_name='Текст сообщения'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создано'
    )

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ('-created_at',)

    def __str__(self):
        return f'Сообщение #{self.pk} (Точка #{self.point_id})'
    
    def clean(self):
        if not self.text.strip():
            raise ValidationError(
                {
                    'text': 'Текст сообщения не может быть пустым.'
                }
            )
