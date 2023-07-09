from rest_framework import routers, permissions
from django.urls import path, include
from web_part.views import MainPage, file_upload, file_export


urlpatterns = [
    path('', MainPage, name='homepage'),
    path('upload/', file_upload, name='file_upload'),
    path('exportCSV/', file_export, name='exportCSV')
]
