from django.contrib import admin

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Административное представление сообщений к гео-точкам."""

    list_display = ('id', 'point', 'author', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('text',)
