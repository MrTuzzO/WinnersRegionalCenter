from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import SupportQuery, SupportReply
from .serializers import SupportQuerySerializer, SupportReplySerializer
from user.permission import IsAdmin, IsAdminOrReadOnly

class SupportQueryViewSet(viewsets.ModelViewSet):
    serializer_class = SupportQuerySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_answered']

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return SupportQuery.objects.all().order_by('-created_at')

        return SupportQuery.objects.filter(user=user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SupportReplyViewSet(viewsets.ModelViewSet):
    serializer_class = SupportReplySerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return SupportReply.objects.all()

    def perform_create(self, serializer):
        reply = serializer.save(admin=self.request.user)

        # Mark query as answered
        query = reply.query
        query.is_answered = True
        query.save()