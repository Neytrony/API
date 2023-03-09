from django.db import models


class BC_TO_YC(models.Model):
    type_proc = models.CharField(max_length=255)
    id_YL = models.CharField(max_length=255)
    id_DOLJNOSTI = models.CharField(max_length=255)


class YC_TO_BC(models.Model):
    type_proc = models.CharField(max_length=255)
    TAB = models.CharField(max_length=255)
    code_study = models.CharField(max_length=255)
