from django.db import models
from django.conf import settings

class EvaluationRequest(models.Model):
    email = models.EmailField()
    full_name = models.CharField(max_length=100)
    massage = models.TextField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.email} - {self.full_name} - {'Approved' if self.is_approved else 'Pending'}"
