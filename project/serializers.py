from rest_framework import serializers
from investment.models import Investment
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class ProjectInvestorSerializer(serializers.ModelSerializer):
    profil_image = serializers.SerializerMethodField()
    class Meta:
        model = Investment
        fields = ( 'id', 'full_name', 'profil_image', 'email', 'phone', 'investment_amount', 'current_country_of_residence', 'created_at', 'status')
        read_only_fields = fields

    def get_profil_image(self, obj):
        request = self.context.get('request')
        if hasattr(obj.user, 'profile_image') and obj.user.profile_image:
            return request.build_absolute_uri(obj.user.profile_image.url)
