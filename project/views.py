from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets
from user.permission import IsAdminOrReadOnly
from rest_framework.pagination import PageNumberPagination
from .serializers import ProjectSerializer
from .models import Project
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at']

    @action(detail=False, methods=['get'], url_path='my_projects', permission_classes=[IsAuthenticated])
    def my_projects(self, request):
        user = request.user
        investments = user.investments.all()
        projects = Project.objects.filter(investments__in=investments).distinct()
        
        page = self.paginate_queryset(projects)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)