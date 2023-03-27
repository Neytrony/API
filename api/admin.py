from django.contrib import admin
from .models import BpToYc, YcToBp

class BpToYcAdmin(admin.ModelAdmin):
    list_display = ['idYL', 'idPos', 'tabNum']

class YcToBpAdmin(admin.ModelAdmin):
    list_display = ['operationType', 'tabNum', 'courseCost']


admin.site.register(BpToYc, BpToYcAdmin)
admin.site.register(YcToBp, YcToBpAdmin)
