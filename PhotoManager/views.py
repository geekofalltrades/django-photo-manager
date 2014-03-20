from django.shortcuts import render
from django.forms import ModelForm
from models import Tag, Photo, Album


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


def frontpage_view(request):
    return render(request, 'PhotoManager/frontpage.html')


def home_view(request):
    pass


def album_view(request):
    pass


def photo_view(request):
    pass


def tag_view(request):
    pass


def login_view(request):
    pass


def logout_view(request):
    pass
