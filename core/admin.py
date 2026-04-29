from django.contrib import admin
from .models import BusinessSetting


@admin.register(BusinessSetting)
class BusinessSettingAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not BusinessSetting.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False