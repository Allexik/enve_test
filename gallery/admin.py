from django.contrib import admin

from . import models


class PhotoInline(admin.TabularInline):
    model = models.Photo


class CommentInline(admin.TabularInline):
    model = models.Comment


class BookmarkInline(admin.TabularInline):
    model = models.Bookmark


@admin.register(models.Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.Album._meta.fields]
    list_editable = [field.name for field in models.Album._meta.fields][1:]
    inlines = (PhotoInline,)


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.Photo._meta.fields]
    list_editable = [field.name for field in models.Photo._meta.fields][1:]
    inlines = (CommentInline,)


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.Comment._meta.fields]
    list_editable = [field.name for field in models.Comment._meta.fields][1:]


@admin.register(models.Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.Bookmark._meta.fields]
    list_editable = [field.name for field in models.Bookmark._meta.fields][1:]
