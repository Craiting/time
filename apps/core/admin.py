	
from django.contrib import admin

from models import TimeEntry,Company,Person,Clocks, Project, EmployeeGroups, EmployeeInGroup, JobCostSave
# Register your models here.

class PersonInline(admin.TabularInline):
    model = Person

class CompanyAdmin(admin.ModelAdmin):
    inlines = [PersonInline]
    list_display = ('company_name','address', 'phone_number')
    search_fields = ['company_name']
    fields = ['company_name', 'address','phone_number']
admin.site.register(JobCostSave)
admin.site.register(Project)
admin.site.register(EmployeeGroups)
admin.site.register(Clocks)
admin.site.register(Company,CompanyAdmin)
admin.site.register(Person)
admin.site.register(EmployeeInGroup)