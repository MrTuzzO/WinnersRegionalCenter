from django.urls import path
from .views import *
from .JCviews import FormSubmitView

urlpatterns = [
    path('business-setting/', BusinessSettingView.as_view(), name='business-setting'),
    path('user/dashboard/', UserDashboardView.as_view(), name='user-dashboard'),
    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('jc-form-submit/', FormSubmitView.as_view(), name='form-submit'),
]