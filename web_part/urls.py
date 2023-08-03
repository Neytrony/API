from django.urls import path
from web_part.views import MainPage, file_import, file_export


urlpatterns = [
    path('', MainPage, name='homepage'),
    path('upload/', file_import, name='file_import'),
    path('export/', file_export, name='export'),
]
