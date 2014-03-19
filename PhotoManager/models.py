from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    """A tag. Any tag can be applied to multiple photos, and those photos
    may have multiple tags.
    """
    text = models.CharField(max_length=32)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.text


def set_upload_to(instance, filename):
    """Determine the folder where an image will be uploaded. Images go
    into folders that are named for their author's primary key id. This
    gives each user a folder while avoiding the problem of usernames that
    contain characters that can't go in file/folder names.
    """
    return '%d/%s' % (instance.author.pk, filename)


class Photo(models.Model):
    """An individual photograph. This photo may exist in many albums and
    have many tags.
    """
    image = models.ImageField(upload_to=set_upload_to)
    description = models.TextField(blank=True)
    author = models.ForeignKey(User)
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title


class Album(models.Model):
    """A photo album. Albums may contain many photos, and these photos django
    not need to be unique to this album.
    """
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    photos = models.ManyToManyField(Photo, blank=True, null=True)
    author = models.ForeignKey(User)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title
