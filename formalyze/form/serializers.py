from rest_framework import serializers
from .models import Form, FormResponse


class FormSerializer(serializers.ModelSerializer):
    creator_name=serializers.SerializerMethodField() #we can retrieve username
    class Meta:
        model = Form
        fields = '__all__'
    
    def get_creator_name(self,obj):
        return f"{obj.created_by.username}"
        
class FormResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormResponse
        fields = '__all__'
        


        



