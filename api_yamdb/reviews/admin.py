from django.contrib import admin

from .models import Title, Review, Category, Genre


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')


class TitleAdmin(admin.ModelAdmin):
    list_display = ('description', 'year', 'category', 'genre')
    search_fields = ('description', 'year', 'category', 'genre')
    list_filter = ('description', 'year', 'category', 'genre')


admin.site.register(Title, TitleAdmin)
admin.site.register(Review)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
