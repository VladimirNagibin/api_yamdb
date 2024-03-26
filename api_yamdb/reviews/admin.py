from django.contrib import admin

from .models import Category, Comments, Genre, Review, Title


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('review', 'text', 'author', 'pub_date')
    search_fields = ('review',)
    list_filter = ('author',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'author', 'score', 'pub_date')
    search_fields = ('title',)
    list_filter = ('author',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'year', 'category', 'genres')
    search_fields = ('name', 'description', 'year')
    list_filter = ('year', 'category')
    filter_horizontal = ('genre',)

    @admin.display(description='Жанры')
    def genres(self, obj):
        return ', '.join([genre.name for genre in obj.genre.all()])
