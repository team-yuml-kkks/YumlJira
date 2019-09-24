from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from .models import User


class UserAdmin(auth_admin.UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': (
            'first_name',
            'last_name',
            'avatar',
        )}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    list_display = (
        'email',
        'username',
        'first_name',
        'last_name',
        'is_superuser',
    )


admin.site.register(User, UserAdmin)

