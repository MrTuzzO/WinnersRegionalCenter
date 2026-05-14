from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class SupportQuery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='queries')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Query #{self.id} by {self.user}"

class SupportReply(models.Model):
    query = models.ForeignKey(SupportQuery, on_delete=models.CASCADE, related_name='replies')
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Reply to Query #{self.query.id} by {self.admin}"