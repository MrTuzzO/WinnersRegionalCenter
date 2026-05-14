from rest_framework import serializers
from .models import Investment


class InvestmentSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = Investment
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'user')

    def get_profile_image(self, obj):
        request = self.context.get('request')
        if hasattr(obj.user, 'profile_image') and obj.user.profile_image:
            return request.build_absolute_uri(obj.user.profile_image.url)
        return None