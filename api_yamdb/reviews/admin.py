from django.contrib import admin

from .models import Title, Review, Category, Genre, Comments
from users.models import User


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('review', 'text', 'author', 'pub_date')
    search_fields = ('review',)
    list_filter = ('author',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'author', 'score', 'pub_date')
    search_fields = ('title',)
    list_filter = ('author',)


class UserAdmin(admin.ModelAdmin):
    list_dispaly = ('__all__',)
    list_filter = ('is_staff', 'role')
    search_fields = ('username',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')


class TitleAdmin(admin.ModelAdmin):
    list_display = ('description', 'year', 'category')
    search_fields = ('description', 'year')
    list_filter = ('year', 'category')
    filter_horizontal = ('genre',)


admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(User, UserAdmin)
