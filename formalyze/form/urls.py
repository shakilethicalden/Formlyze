from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import FormView, FormResponseView

router = DefaultRouter()
router.register('list',FormView)
router.register('response',FormResponseView)


urlpatterns = [
    path('', include(router.urls)),
    
]
