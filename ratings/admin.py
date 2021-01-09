from django.contrib import admin

from .models import User, Title, Genre, Category, Review, Comment


@admin.register(User)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ("name", "year", "category")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("title", "text", "author", "score", "date")
    list_filter = ("title",)
    search_fields = ("title", "text")
