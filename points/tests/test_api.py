from http import HTTPStatus

import pytest

from points.models import Point


pytestmark = pytest.mark.django_db


class TestCreatePointAPI:
    """Тесты API для создания гео-точек."""

    def test_auth_client_can_create_point(
        self,
        auth_client,
        point_form_data,
        routes,
        user
    ):
        """Авторизованный пользователь создать точку."""
        Point.objects.all().delete()
        response = auth_client.post(
            routes['points']['create'],
            data=point_form_data
        )
        assert response.status_code == HTTPStatus.CREATED
        assert Point.objects.count() == 1

        created_point = Point.objects.get()
        assert created_point.title == point_form_data['title']
        assert created_point.location.x == point_form_data['longitude']
        assert created_point.location.y == point_form_data['latitude']
        assert created_point.owner == user

    def test_anonymous_client_cant_create_point(
            self,
            non_auth_client,
            point_form_data,
            routes
    ):
        """Неавторизованный пользователь не может создать точку."""
        Point.objects.all().delete()
        response = non_auth_client.post(
            routes['points']['create'],
            data=point_form_data
        )
        assert response.status_code == HTTPStatus.FORBIDDEN
        assert Point.objects.count() == 0

    @pytest.mark.parametrize(
            'missing_field',
            ('title', 'latitude', 'longitude'),
    )
    def test_cant_create_point_without_required_data(
            self,
            auth_client,
            point_form_data,
            missing_field,
            routes
    ):
        """Невозможно создать точку, если отсутствуют обязательные поля."""
        Point.objects.all().delete()
        copied_data = point_form_data
        copied_data.pop(missing_field)
        response = auth_client.post(
            routes['points']['create'],
            data=copied_data
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert Point.objects.count() == 0

    @pytest.mark.parametrize(
        'field, value',
        (
            ('latitude', -100),
            ('latitude', 100),
            ('longitude', -190),
            ('longitude', 190),
        )
    )
    def test_cant_create_point_with_incorrect_params(
        self,
        auth_client,
        field,
        point_form_data,
        routes,
        value
    ):
        """Нельзя создать точку с параметрами вне диапазона."""
        Point.objects.all().delete()
        copied_data = point_form_data
        copied_data[field] = value
        response = auth_client.post(
            routes['points']['create'],
            data=copied_data
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert Point.objects.count() == 0

    def test_cant_method_get_from_create_point(
            self,
            auth_client,
            routes
    ):
        """Нельзя обратиться к /api/points/ методом GET."""
        response = auth_client.get(routes['points']['create'])
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED


class TestSearchPointAPI:
    """Тесты API для поиска гео-точек."""

    def test_auth_client_can_search(
        self,
        auth_client,
        routes,
        search_data
    ):
        """Авторизованный пользователь может искать точки."""
        response = auth_client.get(
            routes['points']['search'],
            data=search_data
        )
        assert response.status_code == HTTPStatus.OK

    def test_anonymous_client_cant_search(
        self,
        non_auth_client,
        routes,
        search_data
    ):
        """Анонимный пользователь не может искать точки."""
        response = non_auth_client.get(
            routes['points']['search'],
            data=search_data
        )
        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_cant_search_without_params(
            self,
            auth_client,
            routes
    ):
        """Нельзя искать точки без параметров."""
        response = auth_client.get(routes['points']['search'], data={})
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_search_point_return_only_inside_radius(
            self,
            auth_client,
            routes,
            make_point
    ):
        """Поиск точек возвращает только те, которые попадают в радиус"""
        near_point = make_point(longitude=40, latitude=40, title='near')
        far_point = make_point(longitude=90, latitude=90, title='far')

        response = auth_client.get(
            routes['points']['search'],
            data={'latitude': 40.01, 'longitude': 40.01, 'radius': 3}
        )

        assert response.status_code == HTTPStatus.OK

        data = response.json()

        items = data['results'] if (
            isinstance(data, dict) and 'results' in data
        ) else data
        returned_ids = {item['id'] for item in items}

        assert near_point.id in returned_ids
        assert far_point.id not in returned_ids
