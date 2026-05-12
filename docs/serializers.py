from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import RequiredDocument, UserDocument
User = get_user_model()

class UploadStepSerializer(serializers.Serializer):
    signed_file = serializers.FileField(required=True)


class CompletedDocumentSerializer(serializers.Serializer):
    user_document_id = serializers.IntegerField()
    required_document_id = serializers.IntegerField()
    step = serializers.IntegerField()
    title = serializers.CharField()
    download_file = serializers.CharField(allow_blank=True)
    signed_file = serializers.CharField(allow_blank=True)
    status = serializers.CharField()
    reviewed_at = serializers.DateTimeField(allow_null=True)


class CurrentDocumentSerializer(serializers.Serializer):
    user_document_id = serializers.IntegerField(allow_null=True)
    required_document_id = serializers.IntegerField()
    step = serializers.IntegerField()
    title = serializers.CharField()
    download_file = serializers.CharField(allow_blank=True)
    signed_file = serializers.CharField(allow_blank=True, allow_null=True)
    status = serializers.CharField()
    admin_note = serializers.CharField(allow_blank=True)
    submitted_at = serializers.DateTimeField(allow_null=True)
    reviewed_at = serializers.DateTimeField(allow_null=True)
    allow_upload = serializers.BooleanField()


class UserProgressSerializer(serializers.Serializer):
    total_steps = serializers.IntegerField()
    completed_steps = serializers.IntegerField()
    all_completed = serializers.BooleanField()
    current_step = serializers.IntegerField(allow_null=True)
    completed_documents = CompletedDocumentSerializer(many=True)
    current_document = CurrentDocumentSerializer(allow_null=True)


class AdminRequiredDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequiredDocument
        fields = ['id', 'title', 'file', 'step']


class AdminSubmissionSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    user_email = serializers.EmailField(source='user.email', read_only=True)
    step = serializers.IntegerField(source='required_document.step', read_only=True)
    title = serializers.CharField(source='required_document.title', read_only=True)
    download_file = serializers.SerializerMethodField()
    signed_file = serializers.SerializerMethodField()

    class Meta:
        model = UserDocument
        fields = [
            'id', 'user_name', 'user_email', 'step',
            'title', 'download_file', 'signed_file',
            'status', 'admin_note', 'submitted_at', 'reviewed_at',
        ]

    def get_user_name(self, obj):
        full_name = obj.user.get_full_name() if hasattr(obj.user, 'get_full_name') else ''
        if full_name:
            return full_name
        return getattr(obj.user, 'email', str(obj.user))

    def _safe_file_url(self, value, request=None):
        if not value:
            return ''
        try:
            url = value.url
        except Exception:
            name = getattr(value, 'name', '')
            if isinstance(name, bytes):
                name = name.decode('utf-8', errors='replace')
            url = str(name)

        if request is not None and isinstance(url, str) and url.startswith('/'):
            try:
                return request.build_absolute_uri(url)
            except Exception:
                pass
        return url

    def get_download_file(self, obj):
        request = self.context.get('request') if hasattr(self, 'context') else None
        return self._safe_file_url(getattr(obj.required_document, 'file', None), request=request)

    def get_signed_file(self, obj):
        request = self.context.get('request') if hasattr(self, 'context') else None
        return self._safe_file_url(getattr(obj, 'signed_file', None), request=request)


class AdminReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDocument
        fields = ['status', 'admin_note']

    def validate_status(self, value):
        if value not in ('approved', 'rejected'):
            raise serializers.ValidationError("Must be 'approved' or 'rejected'.")
        return value


class AdminUserStepListSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    user_name = serializers.CharField()
    user_email = serializers.CharField(allow_blank=True)
    total_steps = serializers.IntegerField()
    completed_steps = serializers.IntegerField()
    current_step = serializers.IntegerField(allow_null=True)
    status_label = serializers.CharField()


class AdminUserStepDetailSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    user_name = serializers.CharField()
    user_email = serializers.CharField(allow_blank=True)
    total_steps = serializers.IntegerField()
    current_step = serializers.IntegerField(allow_null=True)
    submitted_documents = AdminSubmissionSerializer(many=True)