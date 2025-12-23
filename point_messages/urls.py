from django.urls import path

from .views import MessageCreateView, MessageSearchView


urlpatterns = [
    path('points/messages/', MessageCreateView.as_view(), name='create'),
    path(
        'points/messages/search/',
        MessageSearchView.as_view(),
        name='search'
    ),
]
