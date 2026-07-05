from django.contrib import admin
from .models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category','created_at')
    search_fields = ('title',)
    ordering = ('-created_at',)
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)