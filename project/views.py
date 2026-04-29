from django.shortcuts import render
from rest_framework import viewsets
from user.permission import IsAdminOrReadOnly
from rest_framework.pagination import PageNumberPagination
from .serializers import ProjectSerializer
from .models import Project
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]

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
        return Response(serializer.data)