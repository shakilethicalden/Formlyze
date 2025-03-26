from django.shortcuts import render,redirect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import FormSerializer,FormResponseSerializer
from rest_framework import viewsets,generics,status
from .models import Form, FormResponse

# Create your views here.

class FormView(viewsets.ModelViewSet):
    serializer_class=FormSerializer
    queryset=Form.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'created_by']
 
    
    

            
    
    
    
class FormResponseView(viewsets.ModelViewSet):
    serializer_class=FormResponseSerializer
    queryset=FormResponse.objects.all()
    http_method_names=['get','post']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['form', 'responder_email']
    
    
    #inboke create function for sending mail 
    def create(self,request, *args, **kwargs):
        serializer= self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.save()
            
            subject= "From Submission Confirmation"
            recipient_email=data.responder_email
            sender_email=settings.EMAIL_HOST_USER
            
            html_content= render_to_string("form_response.html",{
                'responder_email':recipient_email,
            })
            
            email= EmailMultiAlternatives(subject, "" , sender_email, [recipient_email])
            email.attach_alternative(html_content, "text/html")
            email.send()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    






