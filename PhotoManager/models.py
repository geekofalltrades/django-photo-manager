from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    """A tag. Any tag can be applied to multiple photos, and those photos
    may have multiple tags.
    """
    text = models.CharField(max_length=32)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.text


class Photo(models.Model):
    """An individual photograph. This photo may exist in many albums and
    have many tags.
    """
    title = models.TextField(max_length=64, default='Untitled')
    timestamp = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    description = models.TextField(blank=True)
    author = models.ForeignKey(User)

    def __unicode__(self):
        return self.title


class Album(models.Model):
    """A photo album. Albums may contain many photos, and these photos django
    not need to be unique to this album.
    """
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    photos = models.ManyToManyField(Photo, blank=True, null=True)
    author = models.ForeignKey(User)

    def __unicode__(self):
        return self.title
