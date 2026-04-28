from django.contrib import admin
from .models import Investment

@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
	list_display = ("user", "project", "full_name", "email", "investment_amount", "investment_strategy", "status", "created_at")
	list_filter = ("status", "investment_strategy", "created_at")
	search_fields = ("full_name", "email", "user__email", "project__name")
	readonly_fields = ("created_at", "updated_at")
