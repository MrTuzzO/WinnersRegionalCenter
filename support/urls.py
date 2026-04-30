from rest_framework.routers import DefaultRouter
from .views import SupportQueryViewSet, SupportReplyViewSet

router = DefaultRouter()
router.register(r'support/queries', SupportQueryViewSet, basename='queries')
router.register(r'support/replies', SupportReplyViewSet, basename='replies')

urlpatterns = router.urls