from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,viewsets
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, LoginSerializer,UserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile


class UserView(viewsets.ModelViewSet):
    serializer_class=UserSerializer
    queryset=UserProfile.objects.all()



class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                try:
                    subject = 'Registration Confirmation'
                    recipient_email = user.email
                    
                    sender_email = settings.EMAIL_HOST_USER
                    
                    html_content = render_to_string("register.html", {
                        'user': user,
                    })
                    
                    email = EmailMultiAlternatives(
                        subject, 
                        "", 
                        sender_email, 
                        [recipient_email]
                    )
                    email.attach_alternative(html_content, "text/html")
                    email.send()
                    
                    return Response({
                        'success': True,
                        "message": "User registered successfully"
                    }, status=status.HTTP_201_CREATED)
                    
                except Exception as e:
                    return Response({
                        'success': True,
                        "message": "User registered but confirmation email failed",
                        "error": str(e)
                    }, status=status.HTTP_201_CREATED)
                    
            except Exception as e:
                return Response({
                    'success': False,
                    "message": "User registration failed",
                    "error": str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        username_or_email = request.data.get('username')
        password = request.data.get('password')

        if not username_or_email or not password:
            return Response({
                'success': False,
                'error': 'Both username/email and password are required.'
            }, status=status.HTTP_400_BAD_REQUEST)

 
        if '@' in username_or_email:
    
            try:
                profile = UserProfile.objects.get(email=username_or_email)
            except UserProfile.DoesNotExist:
                return Response({'error': 'Invalid email', 'success': False},
                                status=status.HTTP_401_UNAUTHORIZED)
        else:
   
            try:
                profile = UserProfile.objects.get(username=username_or_email)
            except UserProfile.DoesNotExist:
                return Response({'error': 'Invalid username', 'success': False},
                                status=status.HTTP_401_UNAUTHORIZED)

 
        user = profile.user
        authenticated_user = authenticate(username=user.username, password=password)

        if authenticated_user:
            token, _ = Token.objects.get_or_create(user=authenticated_user)
            return Response({
                'success': True,
                'user_id': profile.id,
                'message': 'Login successful',
                'token': token.key
            })

        return Response({'error': 'Invalid credentials', 'success': False},
                        status=status.HTTP_401_UNAUTHORIZED)



class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]  
    permission_classes = [IsAuthenticated]  

    def post(self, request):
        try:
            # Delete the token
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"error": "Token not found"}, status=status.HTTP_400_BAD_REQUEST)