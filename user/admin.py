from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import OTP, PasswordResetToken, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
	ordering = ("-created_at",)
	list_display = ("email", "name", "phone_number", "country", "is_email_verified", "is_active", "is_staff", "created_at")
	list_filter = ("is_email_verified", "is_active", "is_staff")
	search_fields = ("email", "name", "phone_number", "country")
	readonly_fields = ("created_at", "updated_at")

	fieldsets = (
		(None, {"fields": ("email", "password")}),
		(_("Personal info"), {"fields": ("name", "phone_number", "profile_image", "date_of_birth", "current_address", "country")}),
		(_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "is_email_verified", "groups", "user_permissions")}),
		(_("Important dates"), {"fields": ("last_login", "created_at", "updated_at")}),
	)
	add_fieldsets = (
		(None, {
			"classes": ("wide",),
			"fields": (
				"email", "name", "phone_number", "profile_image",
				"date_of_birth", "current_address",
				"country", "password1", "password2",
				"is_active", "is_staff", "is_superuser",
				"is_email_verified",
			),
		}),
	)

	def get_fieldsets(self, request, obj=None):
		if not obj:
			return self.add_fieldsets
		return super().get_fieldsets(request, obj)


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
	list_display = ("user", "code", "purpose", "is_used", "attempts", "created_at", "expires_at")
	list_filter = ("purpose", "is_used")
	search_fields = ("user__email", "code")
	readonly_fields = ("created_at", "expires_at")


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
	list_display = ("user", "is_used", "created_at", "expires_at")
	list_filter = ("is_used", 'created_at')
	search_fields = ("user__email", "token_hash")
	readonly_fields = ("token_hash", "created_at", "expires_at")
