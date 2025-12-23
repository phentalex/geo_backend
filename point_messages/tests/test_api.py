from http import HTTPStatus

import pytest

from point_messages.models import Message


pytestmark = pytest.mark.django_db


class TestCreateMessageApi:
    """Тесты API для создания сообщений к гео-точкам."""

    def test_auth_client_can_create_message(
        self,
        auth_client,
        routes,
        point,
        message_form_data,
        user
    ):
        """Авторизованный пользователь может создать сообщение к точке."""
        Message.objects.all().delete()
        response = auth_client.post(
            routes['messages']['create'],
            data=message_form_data
        )
        assert response.status_code == HTTPStatus.CREATED
        assert Message.objects.count() == 1

        msg = Message.objects.get()
        assert msg.text == message_form_data['text']
        assert msg.author == user
        assert msg.point_id == point.id

    def test_anonymous_client_cant_create_comment(
        self,
        non_auth_client,
        routes,
        message_form_data
    ):
        """Аонимный пользтваель не может создать сообщение."""
        Message.objects.all().delete()
        response = non_auth_client.post(
            routes['messages']['create'],
            data=message_form_data
        )
        assert response.status_code == HTTPStatus.FORBIDDEN
        assert Message.objects.count() == 0

    @pytest.mark.parametrize(
            'missing_field',
            ('point_id', 'text')
    )
    def test_cant_create_message_without_required_data(
        self,
        auth_client,
        routes,
        message_form_data,
        missing_field
    ):
        """Нельзя создать сообщение без обязательных полей."""
        Message.objects.all().delete()
        copied_data = message_form_data
        copied_data.pop(missing_field)
        response = auth_client.post(
            routes['messages']['create'],
            data=copied_data
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert Message.objects.count() == 0

    def test_cant_create_message_with_unknown_point(
            self,
            auth_client,
            routes,
            message_form_data
    ):
        """Нельзя создать сообщения для несуществующей точки."""
        Message.objects.all().delete()
        edited_data = message_form_data
        edited_data['point_id'] = 9999
        response = auth_client.post(
            routes['messages']['create'],
            data=edited_data
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert Message.objects.count() == 0

    def test_cant_method_get_from_create_message(self, auth_client, routes):
        """Проверка, что нельзя обратиться к /api/points/ методом GET."""
        response = auth_client.get(routes['messages']['create'])
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED


class TestSearchMessageAPI:
    """Тесты API для поиска сообщений в радиусе."""

    def test_auth_client_can_search_messages(
        self,
        auth_client,
        routes,
        search_data
    ):
        """Авторизованный пользователь может искать сообщения."""
        response = auth_client.get(
            routes['messages']['search'],
            data=search_data
        )
        assert response.status_code == HTTPStatus.OK

    def test_anonymous_client_cant_search_messages(
        self,
        non_auth_client,
        routes,
        search_data
    ):
        """Анонимный пользователь не может искать сообщения."""
        response = non_auth_client.get(
            routes['messages']['search'],
            data=search_data
        )
        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_cant_search_messages_without_params(
            self,
            auth_client,
            routes
    ):
        """Нельзя искать сообщения без параметров."""
        response = auth_client.get(routes['messages']['search'], data={})
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_search_messages_returns_only_inside_radius(
            self,
            auth_client,
            routes,
            make_point,
            make_message
    ):
        """Поиск сообщений возвращает только те, которые попадают в радиус."""
        near_point = make_point(longitude=40, latitude=40, title='near')
        far_point = make_point(longitude=90, latitude=90, title='far')

        near_msg = make_message(point=near_point, text='near msg')
        far_msg = make_message(point=far_point, text='far msg')

        response = auth_client.get(
            routes['messages']['search'],
            data={'latitude': 40.01, 'longitude': 40.01, 'radius': 3}
        )

        assert response.status_code == HTTPStatus.OK

        data = response.json()

        items = data['results'] if (
            isinstance(data, dict) and 'results' in data
        ) else data
        returned_ids = {item['id'] for item in items}

        assert near_msg.id in returned_ids
        assert far_msg.id not in returned_ids
