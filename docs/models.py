from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class RequiredDocument(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='required_docs/')
    step = models.PositiveIntegerField(unique=True)

    class Meta:
        ordering = ['step']

    def __str__(self):
        return f"Step {self.step} - {self.title}"


class UserDocument(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_documents')
    required_document = models.ForeignKey(RequiredDocument, on_delete=models.CASCADE)
    signed_file = models.FileField(upload_to='signed_docs/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    admin_note = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'required_document')
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.user} - Step {self.required_document.step} - {self.status}"