from django.shortcuts import render,redirect
from .serializers import HealthCareSerializer
from rest_framework import viewsets,generics,status
from rest_framework.views import APIView
from .models import HealthCare
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate,login,logout
from rest_framework.authtoken.models import Token
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from rest_framework.authtoken.models import Token

# Create your views here.

class HelthCareView(viewsets.ModelViewSet):
    queryset = HealthCare.objects.all()
    serializer_class = HealthCareSerializer





# class UserListView(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class UserRegisterView(generics.CreateAPIView):
#     serializer_class = UserRegisterSerializer

#     def perform_create(self, serializer):
#         user = serializer.save()
#         token = default_token_generator.make_token(user)
#         uid = urlsafe_base64_encode(force_bytes(user.pk))
#         confirm_link = f'http://127.0.0.1:8000/api/users/activate/{uid}/{token}/'
#         email_subject = 'Activate your account'
#         email_body = render_to_string('confirm_email.html', {'confirm_link': confirm_link})
#         email = EmailMultiAlternatives(email_subject, '', to=[user.email])
#         email.attach_alternative(email_body, 'text/html')
#         email.send()

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             self.perform_create(serializer)
#             return Response({
#                 'success': True,
#                 'message': 'Registration successful! Please check your email to confirm your registration.'
#             }, status=status.HTTP_201_CREATED)
#         else:
#             return Response({
#                 'success': False,
#                 'message': serializer.errors
#             }, status=status.HTTP_400_BAD_REQUEST)

# def activate(request, uid64, token):
#     try:
#         uid = urlsafe_base64_decode(uid64).decode()
#         user = User._default_manager.get(pk=uid)
#     except (User.DoesNotExist, ValueError, OverflowError):
#         user = None

#     if user is not None and default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         return redirect('login')
#     else:
#         return redirect('register')
        
    
   


# class UserLoginView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = UserLoginSerializer(data=request.data)
        
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             password = serializer.validated_data['password']
            
#             print(f"Email: {email}, Password: {password}")  # Debugging the email and password input
            
   
#             try:
#                 user = User.objects.get(email=email)
#                 print(f"User found: {user}")  # Debugging user retrieval
#             except User.DoesNotExist:
#                 return Response({
#                     'success': False,
#                     'message': 'Invalid email or password.'
#                 }, status=status.HTTP_400_BAD_REQUEST)

      
#             user = authenticate(request, username=user.username, password=password)
            
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     token, _ = Token.objects.get_or_create(user=user)  # Correctly using Token.objects
#                     return Response({
#                         'success': True,
#                         'message': 'Login successful!',
#                         'token': token.key,
#                         'user_id': user.id
#                     }, status=status.HTTP_200_OK)
#                 else:
#                     return Response({
#                         'success': False,
#                         'message': 'Your account is not active. Please check your email to activate your account.'
#                     }, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 return Response({
#                     'success': False,
#                     'message': 'Invalid email or password.'
#                 }, status=status.HTTP_400_BAD_REQUEST)

#         return Response({
#             'success': False,
#             'message': 'Invalid data.',
#             'errors': serializer.errors
#         }, status=status.HTTP_400_BAD_REQUEST)
