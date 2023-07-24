from django.contrib import admin
from .models import BpToYc, YcToBp


class BpToYcAdmin(admin.ModelAdmin):
    list_display = ['id', 'SNILS', 'learnCode', 'dateStartLearn', 'tabNum']
    search_fields = ['id', 'SNILS', 'learnCode', 'dateStartLearn', 'tabNum']


class YcToBpAdmin(admin.ModelAdmin):
    list_display = ['id', 'SNILS', 'learnCode', 'dateStartLearn', 'tabNum']
    search_fields = ['id', 'learnCode', 'tabNum', 'bp_to_yc__SNILS', 'bp_to_yc__dateStartLearn']

    def SNILS(self, obj):
        return obj.bp_to_yc.SNILS

    def dateStartLearn(self, obj):
        return obj.bp_to_yc.dateStartLearn






admin.site.register(BpToYc, BpToYcAdmin)
admin.site.register(YcToBp, YcToBpAdmin)
