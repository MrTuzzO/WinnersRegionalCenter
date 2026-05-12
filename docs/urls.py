from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('admin/agreement-forms', views.AdminRequiredDocumentViewSet, basename='forms')

urlpatterns = [
    # User
    path('user/agreement-steps/progress/', views.UserProgressView.as_view()),
    path('user/agreement-steps/current/upload/', views.UserUploadCurrentStepView.as_view()),

    # Admin: user step progress table
    path('admin/user-agreements/', views.AdminUserStepListView.as_view()),
    path('admin/user-agreements/<int:user_id>/', views.AdminUserStepDetailView.as_view()),
    path('admin/user-agreements/step/<int:pk>/review/', views.AdminReviewView.as_view()),
] + router.urls