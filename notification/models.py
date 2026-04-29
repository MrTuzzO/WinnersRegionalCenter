from django.db import models
from django.conf import settings


class Notification(models.Model):
    TARGET_ALL = 'all'
    TARGET_SPECIFIC = 'specific'
    TARGET_CHOICES = [
        (TARGET_ALL, 'All Users'),
        (TARGET_SPECIFIC, 'Specific Users'),
    ]

    title = models.CharField(max_length=255)
    message = models.TextField()
    target = models.CharField(max_length=10, choices=TARGET_CHOICES)
    recipients = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='notifications')
    is_read_by = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='read_notifications')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title