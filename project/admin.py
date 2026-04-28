from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
	list_display = ("name", "city", "status", "created_at")
	list_filter = ("status", "is_eb_5_enabled", "created_at")
	search_fields = ("name", "city", "state")
	readonly_fields = ("created_at", "updated_at")