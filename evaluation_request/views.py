from threading import Thread

from django.conf import settings
from django.core.mail import send_mail
from .serializers import EvaluationRequestSerializer, ContactFormSerializer
from .models import EvaluationRequest
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.throttling import ScopedRateThrottle
from user.permission import IsAdmin
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class EvaluationRequestViewSet(viewsets.ModelViewSet):
    queryset = EvaluationRequest.objects.all()
    serializer_class = EvaluationRequestSerializer
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAdmin()]
    
    def perform_create(self, serializer):
        serializer.save(is_approved=False)
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {"detail": "Your evaluation request has been submitted successfully."}
        return response


class ContactFormView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'contact_form'

    @staticmethod
    def _send_contact_email(data):
        send_mail(
            subject="New Contact Form Submission",
            message=(
                "A new contact form has been submitted.\n\n"
                f"Full Name: {data['full_name']}\n"
                f"Email: {data['email']}\n"
                f"Message: {data['message']}\n"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["khirulislam5750@gmail.com"],
            fail_silently=False,
        )

    def post(self, request, *args, **kwargs):
        serializer = ContactFormSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        try:
            Thread(target=self._send_contact_email, args=(data,), daemon=True).start()
        except Exception:
            return Response(
                {"detail": "Unable to process contact form right now. Please try again shortly."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response(
            {"detail": "Your contact form has been submitted successfully."},
            status=status.HTTP_202_ACCEPTED,
        )