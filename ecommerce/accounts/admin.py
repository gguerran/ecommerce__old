from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from ecommerce.accounts.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = [
        'username', 'is_active', 'is_staff', 'is_superuser'
    ]
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    search_fields = ['username']
    filter_horizontal = ['user_permissions']

    fieldsets = [['Informações pessoais', {'fields': ['username']}]]
    add_fieldsets = [
        ['Informações pessoais', {
            'fields': ['username', 'password1', 'password2']
            }]
    ]


admin.site.unregister(Group)
