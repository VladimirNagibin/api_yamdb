from django.contrib import admin

from .models import Title, Review, Category, Genre, Comments


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


<<<<<<< HEAD
admin.site.register(Title)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Comments, CommentsAdmin)
=======
class UserAdmin(admin.ModelAdmin):
    list_dispaly = ('__all__',)
    list_filter = ('is_staff', 'role')
    search_fields = ('username',)


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


admin.site.register(User, UserAdmin)
>>>>>>> develop
