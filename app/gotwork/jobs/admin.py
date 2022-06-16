from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, JobType, Worker, AvailableTimes, Customer, Owner, Job

class CustomUserAdmin(UserAdmin):
    list_display = ('first_name', 'last_name', 'username', 'email', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('first_name', 'last_name', 'email', 'username')
    readonly_field = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(JobType)
admin.site.register(Worker)
admin.site.register(AvailableTimes)
admin.site.register(Customer)
admin.site.register(Owner)
admin.site.register(Job)