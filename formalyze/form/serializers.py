from rest_framework import serializers
from .models import HealthCare

class HealthCareSerializer(serializers.Serializer):
    class Meta:
        model= HealthCare
        fields = '__all__'
        



