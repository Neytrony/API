from django.contrib import admin
from .models import SoutToAc, SoutFromAc, Employee, RM, ResultMapSOUT, BadFactor, CommissionMember, Protocol


class MultiDBTabularInline(admin.TabularInline):
    using = 'test'

    def get_queryset(self, request):
        # Tell Django to look for inline objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


class MultiDBModelAdmin(admin.ModelAdmin):
    # A handy constant for the name of the alternate database.
    using = 'test'

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


class EmployeeInline(MultiDBTabularInline):
    model = Employee
    extra = 1


class RMInline(MultiDBTabularInline):
    model = RM
    extra = 1


class ResultMapSOUTInline(MultiDBTabularInline):
    model = ResultMapSOUT
    extra = 1


class CommissionMemberInline(MultiDBTabularInline):
    model = CommissionMember
    extra = 1


class ProtocolInline(MultiDBTabularInline):
    model = Protocol
    extra = 1


class BadFactorInline(MultiDBTabularInline):
    model = BadFactor
    extra = 1


class SoutToAcAdmin(MultiDBModelAdmin):
    inlines = (EmployeeInline, RMInline, ResultMapSOUTInline, CommissionMemberInline, )
    list_display = ['cardNum', 'soutAddress']
    search_fields = ['cardNum', 'soutAddress']


class SoutFromAcAdmin(MultiDBModelAdmin):
    inlines = (ProtocolInline, )
    list_display = ['cardNum']
    search_fields = ['cardNum']


class ProtocolAdmin(MultiDBModelAdmin):
    list_display = ['protocolNum', 'protocolDate']
    search_fields = ['protocolNum']


class EmployeeAdmin(MultiDBModelAdmin):
    list_display = ['SNILS', 'fio', 'soutToAc']
    search_fields = ['SNILS', 'surname', 'name', 'secondName', 'birthDate', 'gender', 'invalid']

    def fio(self, obj):
        return f'{obj.surname} {obj.name} {obj.secondName}'


class RMAdmin(MultiDBModelAdmin):
    list_display = ['amountRM', 'numberRM', 'soutToAc']
    search_fields = ['amountRM', 'numberRM', 'soutToAc']


class ResultMapSOUTAdmin(MultiDBModelAdmin):
    inlines = (BadFactorInline,)
    list_display = ['numberSOUT', 'agreementDate', 'workingConditionClass', 'soutToAc']
    search_fields = ['numberSOUT', 'agreementDate', 'workingConditionClass']


class BadFactorAdmin(MultiDBModelAdmin):
    list_display = ['badFactor', 'factorConditionClass', 'resultMapSOUT']
    search_fields = ['badFactor', 'factorConditionClass']


class CommissionMemberAdmin(MultiDBModelAdmin):
    list_display = ['FIO', 'position', 'soutToAc']
    search_fields = ['FIO', 'position']


admin.site.register(SoutToAc, SoutToAcAdmin)
admin.site.register(SoutFromAc, SoutFromAcAdmin)
admin.site.register(Protocol, ProtocolAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(RM, RMAdmin)
admin.site.register(ResultMapSOUT, ResultMapSOUTAdmin)
admin.site.register(BadFactor, BadFactorAdmin)
admin.site.register(CommissionMember, CommissionMemberAdmin)
