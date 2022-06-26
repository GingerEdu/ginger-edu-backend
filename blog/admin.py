from django.contrib import admin

from .models import Post, Tags

# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "author", "created"]


@admin.register(Tags)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "created", "updated"]
