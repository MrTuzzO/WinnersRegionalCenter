from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from user.permission import IsAdmin
from .models import BusinessSetting
from .serializers import BusinessSettingSerializer
from .response import success_response, error_response
from django.core.cache import cache
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from project.models import Project
from investment.models import Investment
from django.db.models import Sum
from evaluation_request.models import EvaluationRequest
from django.db.models import Count, Q
from django.utils import timezone
from django.db.models.functions import TruncMonth
User = get_user_model()

def home(request):
    return HttpResponse("<h1 style='text-align: center; margin-top: 50px;'>Welcome to Winners Regional Center</h1>")

class BusinessSettingView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdmin()]

    def get(self, request):
        obj = cache.get('business_setting')
        if obj is None:
            obj = BusinessSetting.objects.first()
            cache.set('business_setting', obj, timeout=60*60*24)  # 1 day
        return success_response(
            "Business setting fetched successfully.",
            status.HTTP_200_OK,
            data=BusinessSettingSerializer(obj).data if obj else {},
        )

    def post(self, request):
        if BusinessSetting.objects.exists():
            return error_response(
                "Request failed",
                status.HTTP_400_BAD_REQUEST,
                errors={"detail": "Already exists. Use PATCH to update."},
            )
        serializer = BusinessSettingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cache.delete('business_setting')
        return success_response(
            "Business setting created successfully.",
            status.HTTP_201_CREATED,
            data=serializer.data,
        )

    def patch(self, request):
        obj = BusinessSetting.objects.first()
        if not obj:
            return error_response(
                "Request failed",
                status.HTTP_404_NOT_FOUND,
                errors={"detail": "Not found. Use POST to create."},
            )
        serializer = BusinessSettingSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cache.delete('business_setting')
        return success_response(
            "Business setting updated successfully.",
            status.HTTP_200_OK,
            data=serializer.data,
        )
    
# User Dashboard view
class UserDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_investment_amount = Investment.objects.filter(user=request.user).aggregate(total=Sum('investment_amount'))["total"] or 0
        user_projects = Project.objects.filter(investments__user=request.user).values('id', 'status')
        total_projects = user_projects.values('id').distinct().count()
        active_projects = user_projects.filter(status='active').values('id').distinct().count()
        data = {
            "total_investment_amount": total_investment_amount,
            "active_projects": active_projects,
            "total_projects": total_projects
        }
        return success_response("Dashboard fetched successfully.", status.HTTP_200_OK, data=data)
    
class AdminDashboardView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        now = timezone.now()
        start = (now.replace(day=1) - timezone.timedelta(days=365)).replace(day=1)
        qs = (
            User.objects.filter(created_at__gte=start)
            .annotate(month=TruncMonth('created_at'))
            .values('month')
            .order_by('month')
            .annotate(count=Count('id'))
        )
        month_map = {x['month'].strftime('%b').upper(): x['count'] for x in qs}
        months = []
        counts = []
        for i in range(12):
            month = (now.replace(day=1) - timezone.timedelta(days=30*(11-i)))
            label = month.strftime('%b').upper()
            months.append(label)
            counts.append(month_map.get(label, 0))
    
        project_counts = Project.objects.aggregate(
            total_projects=Count('id'),
            active_projects=Count('id', filter=Q(status='active'))
        )
        investment_counts = Investment.objects.aggregate(
            total_investments=Count('id'),
            pending_investments=Count('id', filter=Q(status='pending'))
        )

        total_users = User.objects.count()
        pending_evaluations = EvaluationRequest.objects.filter(is_approved=False).count()

        data = {
            "total_users": total_users,
            "total_projects": project_counts["total_projects"],
            "active_projects": project_counts["active_projects"],
            "pending_investments": investment_counts["pending_investments"],
            "pending_evaluations": pending_evaluations,
            "total_investments": investment_counts["total_investments"],
            "investor_growth": {"labels": months, "data": counts}
        }
        return success_response("Dashboard fetched successfully.", status.HTTP_200_OK, data=data)