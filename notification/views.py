from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema

from core.response import success_response, error_response
from user.permission import IsAdmin
from .models import Notification
from .serializers import NotificationSerializer, SendNotificationSerializer


def get_user_notifications(user):
    return Notification.objects.filter(
        target=Notification.TARGET_ALL
    ) | Notification.objects.filter(
        target=Notification.TARGET_SPECIFIC,
        recipients=user,
    )


class SendNotificationView(APIView):
    permission_classes = [IsAdmin]

    @extend_schema(request=SendNotificationSerializer, responses={201: OpenApiTypes.OBJECT})
    def post(self, request):
        serializer = SendNotificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response("Notification sent.", status.HTTP_201_CREATED)


class MyNotificationView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: NotificationSerializer(many=True)})
    def get(self, request):
        notifications = get_user_notifications(request.user).order_by('-created_at')
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(notifications, request)
        serializer = NotificationSerializer(page, many=True, context={'request': request})
        return success_response(
            "Notifications fetched successfully.",
            status.HTTP_200_OK,
            data=serializer.data,
            count=paginator.page.paginator.count,
            next=paginator.get_next_link(),
            previous=paginator.get_previous_link(),
        )


class UnreadCountView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: OpenApiTypes.OBJECT})
    def get(self, request):
        count = get_user_notifications(request.user).exclude(
            is_read_by=request.user
        ).count()
        return success_response(
            "Unread count fetched successfully.",
            status.HTTP_200_OK,
            data={"unread_count": count},
        )


class MarkReadView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=None, responses={200: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT})
    def post(self, request, pk):
        try:
            notification = get_user_notifications(request.user).get(pk=pk)
        except Notification.DoesNotExist:
            return error_response(
                "Request failed",
                status.HTTP_404_NOT_FOUND,
                errors={"detail": "Not found."},
            )
        notification.is_read_by.add(request.user)
        return success_response("Marked as read.", status.HTTP_200_OK)


class MarkAllReadView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=None, responses={200: OpenApiTypes.OBJECT})
    def post(self, request):
        notifications = get_user_notifications(request.user).exclude(is_read_by=request.user)
        for n in notifications:
            n.is_read_by.add(request.user)
        return success_response("All notifications marked as read.", status.HTTP_200_OK)


class NotificationUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        return Notification.objects.all()