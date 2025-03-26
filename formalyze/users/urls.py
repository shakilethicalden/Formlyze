from django.urls import path,include
from .views import RegisterView, LoginView, LogoutView, UserView
from rest_framework import routers
router= routers.DefaultRouter()
router.register('list',UserView)

urlpatterns = [
    path("", include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/',LogoutView.as_view(), name='logout'), 
]
