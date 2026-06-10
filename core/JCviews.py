import logging
import os
from threading import Thread

from django.core.cache import cache
from django.core.mail import send_mail
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)

RATE_LIMIT_COUNT = 5
RATE_LIMIT_SECONDS = 60 * 10


def get_client_ip(request):
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "unknown")


def is_rate_limited(request):
    cache_key = f"simple_form_submit:{get_client_ip(request)}"

    if cache.add(cache_key, 1, timeout=RATE_LIMIT_SECONDS):
        return False

    request_count = cache.incr(cache_key)
    return request_count > RATE_LIMIT_COUNT


def build_admin_email(data):
    return (
        "A new JC form has been submitted.\n\n"
        f"Name: {data.get('name')}\n"
        f"Email: {data.get('email')}\n"
        f"Phone: {data.get('phone', '')}\n"
        f"Message: {data.get('message')}\n"
    )


def send_form_email_to_admin(data):
    backend_email = os.getenv("EMAIL_HOST_USER")

    if not backend_email:
        raise ValueError("EMAIL_HOST_USER is not configured.")

    send_mail(
        subject="New Form Submission",
        message=build_admin_email(data),
        from_email=backend_email,
        recipient_list=[backend_email],
        # recipient_list=["tuzzo2810@gmail.com"],
        fail_silently=False,
    )


def send_form_email_to_admin_background(data):
    def _send():
        try:
            send_form_email_to_admin(data)
        except Exception:
            logger.exception("Failed to send simple form email")

    Thread(target=_send, daemon=True).start()


class FormSubmitView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        request=inline_serializer(
            name="JobCreatorFormSubmitRequest",
            fields={
                "name": serializers.CharField(max_length=100),
                "email": serializers.EmailField(),
                "phone": serializers.CharField(max_length=20, required=False),
                "message": serializers.CharField(required=False),
            },
        ),
        responses={202: dict, 400: dict, 429: dict, 503: dict},
    )
    def post(self, request):
        if is_rate_limited(request):
            return Response(
                {"detail": "Too many requests. Please try again later."},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        name = request.data.get("name")
        email = request.data.get("email")

        if not name or not email:
            return Response(
                {"detail": "Name and email are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = {
            "name": name,
            "email": email,
            "phone": request.data.get("phone", ""),
            "message": request.data.get("message", ""),
        }

        try:
            send_form_email_to_admin_background(data)
        except Exception:
            return Response(
                {"detail": "Unable to submit form right now."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response(
            {"detail": "Form submitted successfully."},
            status=status.HTTP_202_ACCEPTED,
        )
