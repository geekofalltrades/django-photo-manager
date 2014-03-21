from django.shortcuts import render
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
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
    return render(request, 'PhotoManager/homepage.html')


def album_view(request, id):
    return render(request, 'PhotoManager/album.html')


def photo_view(request, id):
    return render(request, 'PhotoManager/photo.html')


def tag_view(request, id):
    return render(request, 'PhotoManager/tag.html')


def login_view(request):
    return HttpResponseRedirect(reverse('PhotoManager:pm-home'))


def logout_view(request):
    return HttpResponseRedirect(reverse('PhotoManager:pm-front'))
