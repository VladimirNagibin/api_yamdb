from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_dispaly = ('__all__',)
    list_filter = ['is_staff', 'role']
    search_fields = ['username']


admin.site.register(User, UserAdmin)
