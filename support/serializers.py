from rest_framework import serializers
from .models import SupportQuery, SupportReply


class SupportReplySerializer(serializers.ModelSerializer):
    admin = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = SupportReply
        fields = ['id', 'admin', 'message', 'created_at']


class SupportQuerySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    replies = SupportReplySerializer(many=True, read_only=True)

    class Meta:
        model = SupportQuery
        fields = ['id', 'user', 'message', 'is_answered', 'created_at', 'replies']