from django.contrib import admin
from PhotoManager.models import Tag, Photo, Album


class TagAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__',
        'date_created',
    )


class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__',
        'author',
        'date_created',
        'date_modified',
        'description',
    )


class AlbumAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__',
        'author',
        'date_created',
        'date_modified',
        'description',
    )


admin.site.register(Tag, TagAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Album, AlbumAdmin)
