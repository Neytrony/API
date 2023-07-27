from django.contrib import admin
from .models import SoutToAc, SoutFromAc, Employee, RM, ResultMapSOUT, BadFactor, CommissionMember


class EmployeeInline(admin.TabularInline):
    model = Employee
    extra = 1


class RMInline(admin.TabularInline):
    model = RM
    extra = 1


class ResultMapSOUTInline(admin.TabularInline):
    model = ResultMapSOUT
    extra = 1


class CommissionMemberInline(admin.TabularInline):
    model = CommissionMember
    extra = 1


class BadFactorInline(admin.TabularInline):
    model = BadFactor
    extra = 1


class SoutToAcAdmin(admin.ModelAdmin):
    inlines = (EmployeeInline, RMInline, ResultMapSOUTInline, CommissionMemberInline, )
    list_display = ['cardNum', 'soutAddress']
    search_fields = ['cardNum', 'soutAddress']


class SoutFromAcAdmin(admin.ModelAdmin):
    list_display = ['cardNum']
    search_fields = ['cardNum']


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['SNILS', 'fio', 'soutToAc']
    search_fields = ['SNILS', 'surname', 'name', 'secondName', 'birthDate', 'gender', 'invalid']

    def fio(self, obj):
        return f'{obj.surname} {obj.name} {obj.secondName}'


class RMAdmin(admin.ModelAdmin):
    list_display = ['amountRM', 'numberRM', 'soutToAc']
    search_fields = ['amountRM', 'numberRM', 'soutToAc']


class ResultMapSOUTAdmin(admin.ModelAdmin):
    inlines = (BadFactorInline,)
    list_display = ['numberSOUT', 'agreementDate', 'workingConditionClass', 'soutToAc']
    search_fields = ['numberSOUT', 'agreementDate', 'workingConditionClass']


class BadFactorAdmin(admin.ModelAdmin):
    list_display = ['badFactor', 'factorConditionClass', 'resultMapSOUT']
    search_fields = ['badFactor', 'factorConditionClass']


class CommissionMemberAdmin(admin.ModelAdmin):
    list_display = ['FIO', 'position', 'soutToAc']
    search_fields = ['FIO', 'position']


admin.site.register(SoutToAc, SoutToAcAdmin)
admin.site.register(SoutFromAc, SoutFromAcAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(RM, RMAdmin)
admin.site.register(ResultMapSOUT, ResultMapSOUTAdmin)
admin.site.register(BadFactor, BadFactorAdmin)
admin.site.register(CommissionMember, CommissionMemberAdmin)
