from django.urls import path
from .views import BusinessSettingView

urlpatterns = [
    path('business-setting/', BusinessSettingView.as_view(), name='business-setting'),
]