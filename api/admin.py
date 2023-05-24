from django.contrib import admin
from .models import BpToYc, YcToBp

class BpToYcAdmin(admin.ModelAdmin):
    list_display = ['SNILS', 'learnCode', 'dateStartLearn', 'tabNum']
    search_fields = ['SNILS', 'learnCode', 'dateStartLearn', 'tabNum']

class YcToBpAdmin(admin.ModelAdmin):
    list_display = ['SNILS', 'learnCode', 'dateStartLearn', 'tabNum']
    search_fields = ['SNILS', 'learnCode', 'dateStartLearn', 'tabNum']

    def SNILS(self, obj):
        return obj.bp_to_yc.SNILS

    def dateStartLearn(self, obj):
        return obj.bp_to_yc.dateStartLearn

admin.site.register(BpToYc, BpToYcAdmin)
admin.site.register(YcToBp, YcToBpAdmin)
