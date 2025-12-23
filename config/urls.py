from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(('points.urls', 'points'), namespace='points')),
    path('api/', include(
        ('point_messages.urls', 'messages'),
        namespace='messages'
    )),
]
