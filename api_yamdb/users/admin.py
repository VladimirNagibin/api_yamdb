from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .constants import ROLE_CHOICES
from users.models import User


class UserAdmin(BaseUserAdmin):
    list_dispaly = ('__all__',)
    list_filter = ['is_staff', 'role']
    search_fields = ['username']


UserAdmin.fieldsets += (
    ('Роль', {'fields': ('role', )}),
)

admin.site.register(User, UserAdmin)
