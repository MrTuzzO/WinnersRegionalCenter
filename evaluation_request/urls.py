from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import EvaluationRequestViewSet, ContactFormView
router = DefaultRouter()
router.register(r'evaluation-requests', EvaluationRequestViewSet, basename='evaluation-request')

urlpatterns = [
	path('contact/', ContactFormView.as_view(), name='contact-form'),
]

urlpatterns += router.urls
