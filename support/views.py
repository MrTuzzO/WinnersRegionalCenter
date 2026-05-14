from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import SupportQuery, SupportReply
from .serializers import SupportQuerySerializer, SupportReplySerializer
from user.permission import IsAdmin

class UserQueryListCreateView(generics.ListCreateAPIView):
    serializer_class = SupportQuerySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SupportQuery.objects.filter(user=self.request.user).prefetch_related('replies')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AdminQueryListView(generics.ListAPIView):
    serializer_class = SupportQuerySerializer
    permission_classes = [IsAdmin]
    queryset = SupportQuery.objects.prefetch_related('replies')

class AdminReplyCreateView(generics.CreateAPIView):
    serializer_class = SupportReplySerializer
    permission_classes = [IsAdmin]

    def perform_create(self, serializer):
        query = SupportQuery.objects.get(pk=self.kwargs['query_id'])
        serializer.save(admin=self.request.user, query=query)