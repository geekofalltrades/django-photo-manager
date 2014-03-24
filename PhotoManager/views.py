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


class TagPhotoForm(ModelForm):
    class Meta(object):
        model = Photo
        fields = ['tags']


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
    # albums = Album.objects.\
    #     filter(author__exact=request.user.pk).order_by('-date_created')
    albums = Album.objects.all()
    context = {'albums': albums}
    return render(request, 'PhotoManager/homepage.html', context)


def album_view(request, id):
    """View a single album.
    Shows thumbnails of the photos in the album, plus the album's title
    and description, if any.
    """
    album = Album.objects.get(pk=id)
    context = {'album': album}
    return render(request, 'PhotoManager/album.html', context)


def photo_view(request, id):
    """View a single photo.
    Shows the photo, its description (if any), and its tags (if any),
    and allow the user the opportunity to add new tags, including the
    ability to create a completely new tag. A POST to this page signifies
    that the user is adding a tag to this photo.
    """
    photo = Photo.objects.get(pk=id)
    tag_form = TagPhotoForm(instance=photo)
    create_form = TagForm()

    if request.method == 'POST':
        tag_form = TagPhotoForm(request.POST, instance=photo)
        if tag_form.is_valid():
            tag_form.save()
            return HttpResponseRedirect(
                reverse('PhotoManager:pm-photo', args=[photo.pk]))

    context = {
        'photo': photo,
        'tag_form': tag_form,
        'create_form': create_form,
    }
    return render(request, 'PhotoManager/photo.html', context)


def tag_view(request, id):
    """View a list of photos represented by a certain tag.
    Shows thumbnails of the photos with a certain tag applied, which link
    to that photo's page.
    """
    tag = Tag.objects.get(id=id)
    photos = Photo.objects.filter(tags__id=id)
    context = {'photos': photos, 'tag': tag}
    return render(request, 'PhotoManager/tag.html', context)


def create_album_view(request):
    """View that allows users to create an album.
    Presents the user with a form allowing them to initialize album
    details.
    """
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            new_album = form.save(commit=False)
            new_album.author = request.user
            new_album.save()
            for photo in form.cleaned_data['photos']:
                new_album.photos.add(photo)
            new_album.save()
            return HttpResponseRedirect(
                reverse('PhotoManager:pm-album', args=[new_album.pk]))
    else:
        form = AlbumForm()

    context = {'form': form}
    return render(request, 'PhotoManager/create_album.html', context)


def modify_view(request, id):
    """View that allows users to modify an album.
    Presents the user with a form allowing them to change the title or
    description or add or remove photos.
    """
    album = Album.objects.get(pk=id)
    if request.method == 'POST':
        form = AlbumForm(request.POST, instance=album)
        if form.is_valid():
            new_album = form.save()
            return HttpResponseRedirect(
                reverse('PhotoManager:pm-album', args=[new_album.pk]))
    else:
        form = AlbumForm(instance=album)

    context = {'form': form}
    return render(request, 'PhotoManager/modify.html', context)


def create_tag_view(request):
    """View that allows the user to create a new tag.
    This view is reached from the photo view, and so redirects to the
    last photo viewed.
    """
    form = TagForm(request.POST)
    photo = Photo.objects.get(pk=request.POST['photo'])
    if form.is_valid():
        new_tag = form.save()
        photo.tags.add(new_tag)

    return HttpResponseRedirect('PhotoManger:pm-photo', args=[photo.pk])
