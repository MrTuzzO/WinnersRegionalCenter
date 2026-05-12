from django.shortcuts import render
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import InvestmentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import Investment
from user.permission import IsAdmin
from user.utility import is_all_steps_completed
from .serializers import *

class InvestmentViewSet(viewsets.ModelViewSet):
    queryset = Investment.objects.all()
    serializer_class = InvestmentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['full_name', 'email']
    ordering_fields = ['created_at']
    pagination_class = PageNumberPagination
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        else:
            return [IsAuthenticated()]
        
    def perform_create(self, serializer):
        if not is_all_steps_completed(self.request.user):
            raise serializers.ValidationError("You must complete all document steps before investing.")
        serializer.save(user=self.request.user, status='pending')

    def get_queryset(self):
        user = self.request.user    
        if user.is_staff:
            return Investment.objects.all()
        return Investment.objects.filter(user=user)