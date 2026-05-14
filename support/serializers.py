from rest_framework import serializers
from .models import SupportQuery, SupportReply

class SupportReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportReply
        fields = ['id', 'message', 'created_at']

class SupportQuerySerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_profile_image = serializers.SerializerMethodField()
    replies = SupportReplySerializer(many=True, read_only=True)

    class Meta:
        model = SupportQuery
        fields = ['id', 'message', 'created_at', 'user_name', 'user_email', 'user_profile_image', 'replies']

    def get_user_profile_image(self, obj):
        request = self.context.get('request')
        if obj.user.profile_image and hasattr(obj.user.profile_image, 'url'):
            return request.build_absolute_uri(obj.user.profile_image.url)
        return None