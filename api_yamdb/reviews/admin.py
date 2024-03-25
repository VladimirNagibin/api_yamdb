from django.contrib import admin

from .models import Title, Review, Category, Genre, Comments


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('review', 'text', 'author', 'pub_date')
    search_fields = ('review',)
    list_filter = ('author',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'author', 'score', 'pub_date')
    search_fields = ('title',)
    list_filter = ('author',)


admin.site.register(Title)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Comments, CommentsAdmin)
