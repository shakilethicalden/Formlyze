from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import FormView, FormResponseView, form_details


router = DefaultRouter()
router.register('list',FormView, basename='form-list')
router.register('response',FormResponseView, basename='form-response')


urlpatterns = [
    path('', include(router.urls)),
    path('<uuid:unique_token>/', form_details, name='form_details'),

    
]
