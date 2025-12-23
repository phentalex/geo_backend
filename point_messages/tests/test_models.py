import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone

from point_messages.models import Message


pytestmark = pytest.mark.django_db


class TestMessageModel:
    """Тесты модели сообщений к гео-точкам."""

    @pytest.mark.parametrize(
            'text',
            ('Test message',)
    )
    def test_message_can_be_created(
        self,
        make_message,
        point,
        text,
        user
    ):
        """Сообщение создаётся, привязывается к автору и точке"""
        Message.objects.all().delete()
        make_message(author=user, point=point, text=text)
        assert Message.objects.count() == 1

        created_msg = Message.objects.get()
        assert created_msg.point_id == point.id
        assert created_msg.author_id == user.id
        assert created_msg.text == text
        assert created_msg.created_at is not None

    def test_message_created_at_is_set_automatically(
        self,
        make_message,
    ):
        """Поле created_at добавляется автоматически при создании сообщения."""
        before = timezone.now()
        msg = make_message()
        after = timezone.now()
        assert msg.created_at is not None
        assert before <= msg.created_at <= after
