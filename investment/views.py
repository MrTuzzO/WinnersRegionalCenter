from django.shortcuts import render
from rest_framework import viewsets
from .serializers import InvestmentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import Investment
from user.permission import IsAdmin

class InvestmentViewSet(viewsets.ModelViewSet):
    queryset = Investment.objects.all()
    serializer_class = InvestmentSerializer
    pagination_class = PageNumberPagination
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        else:
            return [IsAuthenticated()]
        
    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status='pending')

    def get_queryset(self):
        user = self.request.user    
        if user.is_staff:
            return Investment.objects.all()
        return Investment.objects.filter(user=user)