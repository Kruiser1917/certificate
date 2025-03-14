from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'phone_number', 'birth_date', 'date_created']
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('phone_number', 'birth_date')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация', {'fields': ('phone_number', 'birth_date')}),
    ) 