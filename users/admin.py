from .models import CUser
from django.contrib import admin

class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User',        {'fields': ['email', 'username', 'is_staff', 'is_active']}),
        ('Details',     {'fields': ['birth_date', 'sex', 'date_joined', 'first_name', 'last_name'],
                         'classes': ['collapse']}),
        ]

admin.site.register(CUser, UserAdmin)
