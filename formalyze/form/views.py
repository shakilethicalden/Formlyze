from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse,Http404
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
    
    
    def create(self, request, *args, **kwargs):
        serializer= self.get_serializer(data=request.data)
        if serializer.is_valid():
            form=serializer.save()            
            
            return Response({
                'success': True,
                'form_link': form.get_form_link(),
                'message': 'Form created successfully', }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
           
    
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






def form_details(request,unique_token):
    try:
        form=get_object_or_404(Form,unique_token=unique_token)
    except Form.DoesNotExist:
        raise Http404("Form does not exist")
    
    
    fields=form.fields
    # print(fields)
    
    return render(request, 'form_details.html', {'form': form, 'fields': fields})
        
        
    
    # form_data= {
    #     'title': form.title,
    #     'description': form.description,
    #     'fields': form.fields
    # }
    
    # return JsonResponse(form_data)