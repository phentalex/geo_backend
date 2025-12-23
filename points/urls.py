from django.urls import path

from .views import PointCreateView, PointSearchView


urlpatterns = [
    path('points/', PointCreateView.as_view(), name='create'),
    path('points/search/', PointSearchView.as_view(), name='search'),
]
