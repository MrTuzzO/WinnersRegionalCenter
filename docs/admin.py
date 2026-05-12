# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import RequiredDocument, UserDocument


@admin.register(RequiredDocument)
class RequiredDocumentAdmin(admin.ModelAdmin):
    list_display = ['step', 'title', 'file_preview']
    ordering = ['step']

    def file_preview(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">Download</a>', obj.file.url)
        return '-'
    file_preview.short_description = 'File'


@admin.register(UserDocument)
class UserDocumentAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'step_number', 'title', 'status',
        'signed_file_link',
        'submitted_at', 'reviewed_at'
    ]
    list_filter = ['status', 'required_document__step']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['submitted_at', 'reviewed_at', 'signed_file_link']
    ordering = ['required_document__step']

    fieldsets = (
        ('User & Step', {
            'fields': ('user', 'required_document')
        }),
        ('Submission', {
            'fields': ('signed_file', 'signed_file_link', 'submitted_at')
        }),
        ('Review', {
            'fields': ('status', 'admin_note', 'reviewed_at')
        }),
    )

    def step_number(self, obj):
        return f"Step {obj.required_document.step}"
    step_number.short_description = 'Step'
    step_number.admin_order_field = 'required_document__step'

    def title(self, obj):
        return obj.required_document.title
    title.short_description = 'Form'

    def signed_file_link(self, obj):
        if obj.signed_file:
            return format_html('<a href="{}" target="_blank">Download Signed</a>', obj.signed_file.url)
        return '-'
    signed_file_link.short_description = 'Signed File'