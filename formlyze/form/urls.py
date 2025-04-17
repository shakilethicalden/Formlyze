from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import FormView, FormResponseView, form_details, ExportFormResponsesExcel, ExcelDownloadDetails


router = DefaultRouter()
router.register('list',FormView, basename='form-list')
router.register('response',FormResponseView, basename='form-response')


urlpatterns = [
    path('', include(router.urls)),
    path('<uuid:unique_token>/', form_details, name='form_details'),
    path("export-responses/<int:form_id>/", ExportFormResponsesExcel.as_view(), name="export-responses"),
    path("download-excel/<int:form_id>/", ExcelDownloadDetails.as_view(), name="download-excel"),
    
    
]
