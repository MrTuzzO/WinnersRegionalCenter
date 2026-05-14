from django.urls import path
from .views import UserQueryListCreateView, AdminQueryListView, AdminReplyCreateView

urlpatterns = [
    path('support/queries/', UserQueryListCreateView.as_view()),
    path('support/admin/queries/', AdminQueryListView.as_view()),
    path('support/admin/queries/<int:query_id>/reply/', AdminReplyCreateView.as_view()),
]