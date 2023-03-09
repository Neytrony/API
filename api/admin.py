from django.contrib import admin
from .models import BC_TO_YC, YC_TO_BC

class BC_TO_YC_Admin(admin.ModelAdmin):
    list_display = ['type_proc', 'id_YL', 'id_DOLJNOSTI']

class YC_TO_BC_Admin(admin.ModelAdmin):
    list_display = ['type_proc', 'TAB', 'code_study']


admin.site.register(BC_TO_YC, BC_TO_YC_Admin)
admin.site.register(YC_TO_BC, YC_TO_BC_Admin)
