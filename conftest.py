import pytest
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point as GeoPoint
from django.urls import reverse
from rest_framework.test import APIClient

from point_messages.models import Message
from points.constants import SRID_GPS
from points.models import Point


User = get_user_model()

pytestmark = pytest.mark.django_db


@pytest.fixture
def non_auth_client():
    """Неавторизованный API-клиент."""
    return APIClient()


@pytest.fixture
def user():
    """Тестовый пользователь"""
    return User.objects.create_user(
        username='testuser',
        password='testpassword123'
    )


@pytest.fixture
def point(user):
    return Point.objects.create(
        owner=user,
        title='Текст',
        location=GeoPoint(60.66, 50.55, srid=SRID_GPS)
    )


@pytest.fixture
def auth_client(user):
    """Авторизованный API-клиент."""
    user_client = APIClient()
    user_client.force_login(user)
    return user_client


@pytest.fixture
def make_point(user):
    def _make_point(**kwargs):
        lat = kwargs.pop('latitude', 55.75)
        lon = kwargs.pop('longitude', 37.62)
        return Point.objects.create(
            owner=kwargs.pop("owner", user),
            title=kwargs.pop("title", "Тестовая точка"),
            location=GeoPoint(lon, lat, srid=SRID_GPS),
        )
    return _make_point


@pytest.fixture
def make_message(user, make_point):
    def _make_message(**kwargs):
        point = kwargs.pop('point', make_point())
        return Message.objects.create(
            point=point,
            author=kwargs.pop('author', user),
            text=kwargs.pop('text', 'Тестовое сообщение')
        )
    return _make_message


@pytest.fixture
def point_form_data():
    return {
        'title': 'Тестовая точка',
        'latitude': 55.75,
        'longitude': 37.61
    }


@pytest.fixture
def message_form_data(point):
    return {
        'point_id': point.id,
        'text': 'Привет!'
    }


@pytest.fixture
def search_data():
    return {
        'latitude': 50,
        'longitude': 60,
        'radius': 10000
    }


@pytest.fixture
def routes():
    return {
        'points': {
            'create': reverse('points:create'),
            'search': reverse('points:search'),
        },
        'messages': {
            'create': reverse('messages:create'),
            'search': reverse('messages:search'),
        }
    }
