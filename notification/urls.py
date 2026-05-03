from django.urls import path
from .views import *

urlpatterns = [
    path('notification/send/', SendNotificationView.as_view(), name='notification-send'),
    path('notification/my/', MyNotificationView.as_view(), name='notification-my'),
    path('notification/my/unread-count/', UnreadCountView.as_view(), name='notification-unread-count'),
    path('notification/my/<int:pk>/read/', MarkReadView.as_view(), name='notification-read'),
    path('notification/my/read-all/', MarkAllReadView.as_view(), name='notification-read-all'),
    path('notification/<int:pk>/', NotificationUpdateDeleteView.as_view(), name='notification-update-delete'),
]   