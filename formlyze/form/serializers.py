from rest_framework import serializers
from .models import Form, FormResponse



class FormSerializer(serializers.ModelSerializer):
    creator_name=serializers.SerializerMethodField() #we can retrieve username
    form_link = serializers.SerializerMethodField()
    class Meta:
        model = Form
        fields = '__all__'

        
    def get_form_link(self,obj):
        return obj.get_form_link()
    
    def get_creator_name(self,obj):
        return f"{obj.created_by.username}"
        
class FormResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormResponse
        fields = '__all__'
        


        



