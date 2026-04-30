from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/docs/', SpectacularSwaggerView.as_view(url_name='schema')),

    path('api/v1/auth/', include('user.urls')),
    path('api/v1/', include('core.urls')),
    path('api/v1/', include('evaluation_request.urls')),
    path('api/v1/', include('project.urls')),
    path('api/v1/', include('investment.urls')),
    path('api/v1/', include('notification.urls')),
    path('api/v1/', include('support.urls')),
]
