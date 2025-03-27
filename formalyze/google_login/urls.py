from django.urls import path
from .views import GoogleLogin, GoogleLoginCallback, LoginPage,LogoutView

urlpatterns = [
    path("goggle/login/", LoginPage.as_view(), name="login"),
    path("v1/auth/google/", GoogleLogin.as_view(), name="google_login"),
    path("v1/auth/google/callback/", GoogleLoginCallback.as_view(), name="google_login_callback"),
    path('goggle/logout/', LogoutView.as_view(), name='logout'),
]
