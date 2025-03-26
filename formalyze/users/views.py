from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,viewsets
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, LoginSerializer,UserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class UserView(viewsets.ModelViewSet):
    serializer_class=UserSerializer
    queryset=User.objects.all()



class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                "message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            
            if user:
                
                # Generate or retrieve the token
                token, _ = Token.objects.get_or_create(user=user)
                return Response({
                    'success': True,
                    'user_id': user.id,
                    'message': 'Login successful',
                    'token': token.key
                })
            
            return Response({'error': 'Invalid credentials',
                             'success': False }, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




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