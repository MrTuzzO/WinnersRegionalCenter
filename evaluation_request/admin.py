from django.contrib import admin
from .models import EvaluationRequest

@admin.register(EvaluationRequest)
class EvaluationRequestAdmin(admin.ModelAdmin):
	list_display = ("email", "full_name", "is_approved", "created_at", "updated_at")
	list_filter = ("is_approved", "created_at")
	search_fields = ("email", "full_name")
	readonly_fields = ("created_at", "updated_at")
