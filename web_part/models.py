from django.db import models
from django.core.files.storage import FileSystemStorage

# Create your models here.
class Files(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    fileField = models.FileField(upload_to='', null=True, blank=True, verbose_name="Файл", storage=FileSystemStorage)
    task_id = models.CharField(max_length=255, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    type = models.PositiveIntegerField()
    status = models.CharField(max_length=255, null=True, blank=True)
