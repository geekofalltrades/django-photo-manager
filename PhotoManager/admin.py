from django.contrib import admin
from PhotoManager.models import Tag, Photo, Album


class TagAdmin(admin.ModelAdmin):
    pass


class PhotoAdmin(admin.ModelAdmin):
    pass


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'timestamp', 'description', 'author')


admin.site.register(Tag)
admin.site.register(Photo)
admin.site.register(Album, AlbumAdmin)