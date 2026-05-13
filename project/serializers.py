from rest_framework import serializers
from investment.models import Investment
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class ProjectInvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = ( 'id', 'full_name', 'email', 'phone', 'investment_amount', 'current_country_of_residence', 'created_at', 'status')
        read_only_fields = fields
