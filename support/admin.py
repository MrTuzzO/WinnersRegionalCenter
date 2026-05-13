from django.contrib import admin
from .models import SupportQuery, SupportReply

@admin.register(SupportQuery)
class SupportQueryAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'message', 'is_answered', 'created_at', 'updated_at')
	list_filter = ('is_answered', 'created_at', 'updated_at')
	search_fields = ('user__username', 'user__email', 'message')
	date_hierarchy = 'created_at'
	ordering = ('-created_at',)

@admin.register(SupportReply)
class SupportReplyAdmin(admin.ModelAdmin):
	list_display = ('id', 'query', 'admin', 'message', 'created_at')
	list_filter = ('created_at',)
	search_fields = ('query__id', 'admin__username', 'admin__email', 'message')
	date_hierarchy = 'created_at'
	ordering = ('-created_at',)
