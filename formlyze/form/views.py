from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from rest_framework.views import APIView
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import FormSerializer,FormResponseSerializer
from rest_framework import viewsets,generics,status
from .models import Form, FormResponse
from django.contrib import messages
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework.response import Response
from django.http import FileResponse
from .utils.export_excel import generate_excel

def is_valid_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


# Create your views here.

class FormView(viewsets.ModelViewSet):
    serializer_class=FormSerializer
    queryset = Form.objects.all().order_by('-created_at')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'created_by']
    # permission_classes=[IsAuthenticated]
    
    
    def create(self, request, *args, **kwargs):
        serializer= self.get_serializer(data=request.data)
        if serializer.is_valid():
            form=serializer.save()
            
            subject= "Form Creation Confirmation"
            recipient_email=form.created_by.email
            sender_email=settings.EMAIL_HOST_USER
            
            html_content= render_to_string("form_creation.html",{
                'form':form,
                'username':form.created_by.username
                
            })
            
            email= EmailMultiAlternatives(subject, "" , sender_email, [recipient_email])
            email.attach_alternative(html_content, "text/html")
            email.send()
            
                        
            
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
            
            response_url=f"{settings.FRONTEND_URL}/view-single-response/{data.id}"
            subject= "From Submission Confirmation"
            creator_email=data.form.created_by.email
            responder_email=data.responder_email
            sender_email=settings.EMAIL_HOST_USER
            #send mail to creator
            if is_valid_email(creator_email):
                try:
                    html_content= render_to_string("form_response_creator.html",{
                        'username':data.form.created_by.username,
                        'form_title':data.form.title, 
                        'response_url':response_url
                    })

                    email= EmailMultiAlternatives(subject, "" , sender_email, [creator_email])
                    email.attach_alternative(html_content, "text/html")
                    email.send()
                except Exception as e:
                    return Response({"error": "Failed to send email to creator"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Invalid email address"}, status=status.HTTP_400_BAD_REQUEST)
            
            #send mail to responder
            if is_valid_email(responder_email):
                try:
                    html_content= render_to_string("form_response.html",{
                        'responder_email':responder_email, 
                        'response_url':response_url
                    })

                    email= EmailMultiAlternatives(subject, "" , sender_email, [responder_email])
                    email.attach_alternative(html_content, "text/html")
                    email.send()
                except Exception as e:
                    return Response({"error": "Failed to send email to responder"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Invalid email address"}, status=status.HTTP_400_BAD_REQUEST)
            
            
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    






def form_details(request, unique_token):
    form = get_object_or_404(Form, unique_token=unique_token)
    fields = form.fields  

    return JsonResponse({'id': form.id, 'form_name': form.title, 'fields': fields}) #return json response just form name and fields
        
        
        
        
        
class ExportFormResponsesExcel(APIView):


    def get(self, request, form_id):
        try:
            form_responses = FormResponse.objects.filter(form_id=form_id)
            form = Form.objects.get(id=form_id)
            # print(form_responses)
            excel_file = generate_excel(form_responses)

            filename = f"{form.title}_responses.xlsx" #excel file save for this name
            response = FileResponse(
                excel_file,
                as_attachment=True,
                filename=filename,
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            return response
        except Form.DoesNotExist:
            return Response({"error": "Something wrong maybe check your form id"}, status=status.HTTP_404_NOT_FOUND)
    
    


class ExcelDownloadDetails(APIView):
    
    def get(self, request, form_id):
        form = get_object_or_404(Form, id=form_id)
        url=f"http://127.0.0.1:8000/api/form/export-responses/{form_id}/"
        return Response({
            "form_title": form.title,
            'url': url})
            