from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'bio', 'role',)
    list_filter = ('is_staff', 'role')
    search_fields = ('username',)
    list_editable = ('role',)
