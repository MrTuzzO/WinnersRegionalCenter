from django.shortcuts import render
from rest_framework import viewsets
from user.permission import IsAdminOrReadOnly
from rest_framework.pagination import PageNumberPagination
from .serializers import ProjectSerializer
from .models import Project

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]