from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
class SupportQuery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='queries')
    message = models.TextField()
    is_answered = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Query {self.id} - {self.user}"
    
class SupportReply(models.Model):
    query = models.ForeignKey(SupportQuery, on_delete=models.CASCADE, related_name='replies')
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies')

    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply {self.id} to Query {self.query.id} by {self.admin}"
