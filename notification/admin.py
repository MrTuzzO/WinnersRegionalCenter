from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'target', 'created_at')
    list_filter = ('target',)
    filter_horizontal = ('recipients', 'is_read_by')
    readonly_fields = ('is_read_by', 'created_at')