from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import EvaluationRequestViewSet
router = DefaultRouter()
router.register(r'evaluation-requests', EvaluationRequestViewSet, basename='evaluation-request')

urlpatterns = router.urls
