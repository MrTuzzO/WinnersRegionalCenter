from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets
from user.permission import IsAdmin, IsAdminOrReadOnly
from .serializers import ProjectInvestorSerializer, ProjectSerializer
from .models import Project
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import OpenApiParameter, extend_schema

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['name', 'short_description']
    ordering_fields = ['created_at']

    @extend_schema(
        summary="List user's projects",
        description="Returns the list of projects the authenticated user has invested in. Supports filtering by project status and investment status.",
        parameters=[
            OpenApiParameter(
                name="project_status",
                type=str,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Filter by project status (active, completed)"
            ),
            OpenApiParameter(
                name="investment_status",
                type=str,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Filter by investment status (pending, approved, rejected)"
            ),
        ],
        responses={200: ProjectSerializer(many=True)},
    )
    @action(detail=False, methods=['get'], url_path='my_projects', permission_classes=[IsAuthenticated])
    def my_projects(self, request):
        user = request.user
        project_status = request.query_params.get('project_status')
        investment_status = request.query_params.get('investment_status')

        investments = user.investments.all()
        if investment_status:
            investments = investments.filter(status=investment_status)

        projects = Project.objects.filter(investments__in=investments)
        if project_status:
            projects = projects.filter(status=project_status)
        projects = projects.distinct()

        page = self.paginate_queryset(projects)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='investors', permission_classes=[IsAdmin])
    def investors(self, request, pk=None):
        project = self.get_object()
        investments = project.investments.filter(status='approved').order_by('-created_at')

        page = self.paginate_queryset(investments)
        if page is not None:
            serializer = ProjectInvestorSerializer(page, many=True, context=self.get_serializer_context())
            return self.get_paginated_response(serializer.data)

        serializer = ProjectInvestorSerializer(investments, many=True, context=self.get_serializer_context())
        return Response(serializer.data, status=status.HTTP_200_OK)
