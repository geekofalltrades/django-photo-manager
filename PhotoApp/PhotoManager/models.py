from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    """A tag. Any tag can be applied to multiple photos, and those photos
    may have multiple tags.
    """
    text = models.CharField(max_length=32)
    timestamp = models.DateTimeField(auto_now_add=True)


class Photo(models.Model):
    """An individual photograph. This photo may exist in many albums and
    have many tags.
    """
    timestamp = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    description = models.TextField()
    author = models.ForeignKey(User)


class Album(models.Model):
    """A photo album. Albums may contain many photos, and these photos django
    not need to be unique to this album.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    photos = models.ManyToManyField(Photo)
    author = models.ForeignKey(User)
