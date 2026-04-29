from django.db import models

class EvaluationRequest(models.Model):
    email = models.EmailField()
    full_name = models.CharField(max_length=100)
    message = models.TextField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.pk:
            previous = EvaluationRequest.objects.filter(pk=self.pk).values("is_approved").first()
            just_approved = previous and not previous["is_approved"] and self.is_approved
        else:
            just_approved = False

        super().save(*args, **kwargs)

        if just_approved:
            self._provision_user()

    def _provision_user(self):
        from django.conf import settings
        from django.core.mail import send_mail
        from user.models import User

        name = self.full_name or self.email.split("@")[0]

        user, created = User.objects.get_or_create(
            email=self.email,
            defaults={"name": name},
        )

        if created:
            user.set_unusable_password()
            user.is_email_verified = True
            user.save(update_fields=["password", "is_email_verified"])

        send_mail(
            subject="Your account has been approved",
            message=(
                f"Hi {user.name},\n\n"
                f"Your evaluation request has been approved and your account is ready.\n\n"
                f"To get started, set your password using the following steps:\n\n"
                f"    Email: {user.email}\n\n"
                f"Go to the login page and click 'Forgot Password' to set your password.\n\n"
                "Welcome aboard!"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

    def __str__(self):
        return f"{self.email} - {self.full_name} - {'Approved' if self.is_approved else 'Pending'}"