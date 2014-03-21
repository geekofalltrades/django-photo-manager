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
    """View the front page of the website.
    Displays welcome text and links that prompt the user to either login
    or register.
    """
    return render(request, 'PhotoManager/frontpage.html')


def home_view(request):
    """View the home page.
    Shows a list of the user's albums with title and description.
    """
    albums = Album.objects.\
        filter(author__exact=request.user.pk).order_by('-date_created')
    context = {'albums': albums}
    return render(request, 'PhotoManager/homepage.html', context)


def album_view(request, id):
    """View a single album.
    Shows thumbnails of the photos in the album, plus the album's title
    and description, if any.
    """
    album = Album.objects.filter(id__exact=id)
    context = {'album': album}
    return render(request, 'PhotoManager/album.html', context)


def photo_view(request, id):
    """View a single photo.
    Shows the photo, its description (if any), and its tags (if any),
    and allow the user the opportunity to add new tags, including the
    ability to create a completely new tag.
    """
    photo = Photo.objects.filter(id__exact=id)
    context = {'photo': photo}
    return render(request, 'PhotoManager/photo.html', context)


def tag_view(request, id):
    """View a list of photos represented by a certain tag.
    Shows thumbnails of the photos with a certain tag applied, which link
    to that photo's page.
    """
    photos = Photo.objects.filter(tags__id__exact=id)
    context = {'photos': photos}
    return render(request, 'PhotoManager/tag.html', context)


def create_album_view(request):
    """View that allows users to create an album.
    Presents the user with a form allowing them to initialize album
    details.
    """
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse('PhotoManager:pm-album', args=))
    else:
        return render(request, 'PhotoManager/create_album.html')


def add_view(request):
    """View that allows users to add a photo to an album.
    Presents the user with a form allowing them to select additional photos
    for the given album.
    """
    return render(request, 'PhotoManager/add.html')


def create_tag_view(request):
    """View submitted to when the user creates a new tag.
    Creates a new tag, then redirects the user to the page from which
    they came.
    """
    return HttpResponseRedirect(reverse('page_user_came_from'))
