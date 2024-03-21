from django.contrib import admin

from .models import Title
from .models import Review


admin.site.register(Title)
admin.site.register(Review)
