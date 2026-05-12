from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('admin/forms', views.AdminRequiredDocumentViewSet, basename='forms')

urlpatterns = [
    # User
    path('agreement-steps/progress/', views.UserProgressView.as_view()),
    path('agreement-steps/current/upload/', views.UserUploadCurrentStepView.as_view()),

    # Admin: user step progress table
    path('admin/users-agreement/', views.AdminUserStepListView.as_view()),
    path('admin/users-agreement/<int:user_id>/', views.AdminUserStepDetailView.as_view()),
    path('admin/agreement-steps/<int:pk>/review/', views.AdminReviewView.as_view()),
] + router.urls