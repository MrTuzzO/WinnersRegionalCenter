from django.shortcuts import render
from .serializers import EvaluationRequestSerializer
from .models import EvaluationRequest
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from user.permission import IsAdmin
from rest_framework.pagination import PageNumberPagination


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