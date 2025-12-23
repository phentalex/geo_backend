from django.contrib import admin

from .models import Point


@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    """Административное представление гео-точек."""

    list_display = ('id', 'title', 'owner', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title',)
