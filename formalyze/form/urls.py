from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import HelthCareView

router = DefaultRouter()
router.register('list',HelthCareView)


urlpatterns = [
    path('', include(router.urls)),
    
]
