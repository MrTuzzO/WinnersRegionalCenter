from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    is_read = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ('id', 'title', 'message', 'created_at', 'is_read')

    def get_is_read(self, obj) -> bool:
        user = self.context['request'].user
        return obj.is_read_by.filter(pk=user.pk).exists()


class SendNotificationSerializer(serializers.ModelSerializer):
    recipient_ids = serializers.ListField(child=serializers.IntegerField(), required=False)

    class Meta:
        model = Notification
        fields = ('title', 'message', 'target', 'recipient_ids')

    def validate(self, attrs):
        if attrs['target'] == Notification.TARGET_SPECIFIC and not attrs.get('recipient_ids'):
            raise serializers.ValidationError({"recipient_ids": "Required when target is 'specific'."})
        if attrs['target'] == Notification.TARGET_ALL:
            attrs['recipient_ids'] = []
        return attrs

    def create(self, validated_data):
        from user.models import User
        recipient_ids = validated_data.pop('recipient_ids', [])
        notification = Notification.objects.create(**validated_data)
        if notification.target == Notification.TARGET_SPECIFIC:
            users = User.objects.filter(pk__in=recipient_ids)
            notification.recipients.set(users)
        return notification
