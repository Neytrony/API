from django.urls import path
from web_part.views import MainPage, file_import, file_export_csv, file_export_xlsx


urlpatterns = [
    path('', MainPage, name='homepage'),
    path('upload/', file_import, name='file_import'),
    path('exportCSV/', file_export_csv, name='exportCSV'),
    path('exportXLSX/', file_export_xlsx, name='exportXLSX'),
]
