from rest_framework import routers, permissions
from django.urls import path, include
from web_part.views import MainPage, file_upload, file_export_csv, file_export_xlsx


urlpatterns = [
    path('', MainPage, name='homepage'),
    path('upload/', file_upload, name='file_upload'),
    path('exportCSV/', file_export_csv, name='exportCSV'),
    path('exportXLSX/', file_export_xlsx, name='exportXLSX'),
]
