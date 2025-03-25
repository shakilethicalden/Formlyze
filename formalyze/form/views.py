from django.shortcuts import render,redirect
from .serializers import FormSerializer,FormResponseSerializer
from rest_framework import viewsets,generics,status
from .models import Form, FormResponse

# Create your views here.

class FormView(viewsets.ModelViewSet):
    serializer_class=FormSerializer
    queryset=Form.objects.all()
    
class FormResponseView(viewsets.ModelViewSet):
    serializer_class=FormResponseSerializer
    queryset=FormResponse.objects.all()






