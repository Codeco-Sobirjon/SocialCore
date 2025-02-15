from django.contrib import admin

from apps.blog.models import (
    Blog, Directory, BlogViews, BlogImage
)


class BlogViewsTableInlines(admin.TabularInline):
    model = BlogViews
    extra = 1


class BlogImageTableInlines(admin.TabularInline):
    model = BlogImage
    extra = 1


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at']
    list_filter = ['medical_illness']
    inlines = [BlogImageTableInlines, BlogViewsTableInlines]


@admin.register(Directory)
class DirectoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at']
