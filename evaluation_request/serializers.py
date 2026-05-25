from rest_framework import serializers
from .models import EvaluationRequest

class EvaluationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationRequest
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class ContactFormSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    message = serializers.CharField()
