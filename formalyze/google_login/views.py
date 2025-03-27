from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
import requests
import jwt

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_OAUTH_CALLBACK_URL
    client_class = OAuth2Client

class GoogleLoginCallback(APIView):
    def get(self, request, *args, **kwargs):
        code = request.GET.get("code")
        if not code:
            return Response({"error": "No authorization code provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Exchange code for tokens
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_OAUTH_CALLBACK_URL,
            "grant_type": "authorization_code",
        }
        response = requests.post(token_url, data=data)
        if response.status_code != 200:
            return Response({"error": "Failed to exchange token", "details": response.json()}, status=status.HTTP_400_BAD_REQUEST)

        tokens = response.json()
        id_token = tokens.get("id_token")

        # Decode ID Token
        try:
            decoded_token = jwt.decode(id_token, options={"verify_signature": False})
        except jwt.ExpiredSignatureError:
            return Response({"error": "ID token has expired"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid ID token"}, status=status.HTTP_400_BAD_REQUEST)

        # Extract user info
        email = decoded_token.get("email")
        first_name = decoded_token.get("given_name", "")
        last_name = decoded_token.get("family_name", "")
        if not email:
            return Response({"error": "No email found in ID token"}, status=status.HTTP_400_BAD_REQUEST)

        user, _ = User.objects.get_or_create(username=email, defaults={"email": email, "first_name": first_name, "last_name": last_name}) # user get and create

        # Generate JWT token
        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh_token": str(refresh),
            "access_token": str(refresh.access_token),
            "user": {"id": user.id, "email": user.email, "first_name": user.first_name, "last_name": user.last_name},
        }, status=status.HTTP_200_OK)

class LoginPage(View):
    def get(self, request, *args, **kwargs):
        return render(request, "login.html", {"google_callback_uri": settings.GOOGLE_OAUTH_CALLBACK_URL, "google_client_id": settings.GOOGLE_OAUTH_CLIENT_ID})


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            logout(request)
            return Response({"message": f"Successfully logged out, {user.username}."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No user is currently logged in."}, status=status.HTTP_400_BAD_REQUEST)