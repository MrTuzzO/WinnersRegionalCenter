from django.urls import path
from .views import *

urlpatterns = [
    path('business-setting/', BusinessSettingView.as_view(), name='business-setting'),
    path('user/dashboard/', UserDashboardView.as_view(), name='user-dashboard'),
    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
]