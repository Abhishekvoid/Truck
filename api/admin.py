
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Organization, HmiGroup, HMI


class CustomUserAdmin(UserAdmin):
   
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('organization', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('organization', 'role')}),
    )

class HMIAdmin(admin.ModelAdmin):
    fields = ['name', 'organization', 'groups', 'assigned_workers']

admin.site.register(Organization)
admin.site.register(HmiGroup)
admin.site.register(User, CustomUserAdmin)

admin.site.register(HMI, HMIAdmin)