from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from user.permission import IsAdmin
from .models import BusinessSetting
from .serializers import BusinessSettingSerializer
from django.core.cache import cache

class BusinessSettingView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdmin()]

    def get(self, request):
        obj = cache.get('business_setting')
        if obj is None:
            obj = BusinessSetting.objects.first()
            cache.set('business_setting', obj, timeout=60*60*24)  # 1 day
        return Response(BusinessSettingSerializer(obj).data if obj else {})

    def post(self, request):
        if BusinessSetting.objects.exists():
            return Response({"detail": "Already exists. Use PATCH to update."}, status=400)
        serializer = BusinessSettingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cache.delete('business_setting')
        return Response(serializer.data, status=201)

    def patch(self, request):
        obj = BusinessSetting.objects.first()
        if not obj:
            return Response({"detail": "Not found. Use POST to create."}, status=404)
        serializer = BusinessSettingSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cache.delete('business_setting')
        return Response(serializer.data)