import logging
from threading import Thread

from django.db import models, transaction


logger = logging.getLogger(__name__)

class EvaluationRequest(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    message = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if self.pk:
            previous = EvaluationRequest.objects.filter(pk=self.pk).values("is_approved").first()
            just_approved = previous and not previous["is_approved"] and self.is_approved
        else:
            just_approved = False

        super().save(*args, **kwargs)

        if is_new:
            transaction.on_commit(self._notify_wrc_submission)

        if just_approved:
            transaction.on_commit(self._provision_user)

    def _send_mail_in_background(self, **mail_kwargs):
        from django.core.mail import send_mail

        def _send():
            try:
                send_mail(**mail_kwargs)
            except Exception:
                logger.exception("Failed to send evaluation request email")

        Thread(target=_send, daemon=True).start()

    def _notify_wrc_submission(self):
        from django.conf import settings

        self._send_mail_in_background(
            subject="New Evaluation Request Submitted",
            message=(
                "A new evaluation request has been submitted.\n\n"
                f"Full Name: {self.full_name}\n"
                f"Email: {self.email}\n"
                f"Phone: {self.phone or 'N/A'}\n"
                f"Message: {self.message or 'N/A'}\n"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["khirulislam5750@gmail.com"],
            fail_silently=False,
        )

    def _provision_user(self):
        from django.conf import settings
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

        self._send_mail_in_background(
            subject="Your account has been approved",
            message=(
                f"Hi {user.name},\n\n"
                f"Your evaluation request has been approved and your account is ready.\n\n"
                f"To get started, set your password using the following steps:\n\n"
                f"    Email: {user.email}\n\n"
                f"Go to the login page and click 'Forgot Password' to set your password.\n\n"
                "Welcome to Winners Regional Center!"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

    def __str__(self):
        return f"{self.email} - {self.full_name} - {'Approved' if self.is_approved else 'Pending'}"