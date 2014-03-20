from django.shortcuts import render
from models import Tag, Photo, Album
from django.forms import ModelForm


class TagForm(ModelForm):
    class Meta(object):
        model = Tag
        fields = ['text']


class PhotoForm(ModelForm):
    class Meta(object):
        model = Photo
        fields = ['image', 'description', 'tags']


class AlbumForm(ModelForm):
    class Meta(object):
        model = Album
        fields = ['title', 'description', 'photos']


def frontpage_view():
    pass


def home_view():
    pass


def album_view():
    pass


def photo_view():
    pass


def tag_view():
    pass


def login_view():
    pass


def logout_view():
    pass
