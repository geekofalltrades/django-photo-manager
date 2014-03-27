from django.shortcuts import render
from django.forms import ModelForm
from django.http import HttpResponseRedirect, HttpResponseForbidden, \
    HttpResponseNotAllowed
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from models import Tag, Photo, Album


class TagForm(ModelForm):
    class Meta(object):
        model = Tag
        fields = ['text']


class CreatePhotoForm(ModelForm):
    """The CreatePhotoForm allows users to upload an image to associate
    with this photo.
    """
    class Meta(object):
        model = Photo
        fields = ['image', 'description', 'tags']


class EditPhotoForm(ModelForm):
    """The EditPhotoForm does not allow users to change the image associated
    with this photo object.
    """
    class Meta(object):
        model = Photo
        fields = ['description', 'tags']


class AlbumForm(ModelForm):
    def __init__(self, *args, **kwargs):
        """Custom constructor that filters the queryset available to the
        photos form to restrict it to the currently logged-in user.
        """
        authorized_user = kwargs.pop('authorized_user')
        super(AlbumForm, self).__init__(*args, **kwargs)
        self.fields['photos'].queryset = \
            Photo.objects.filter(author=authorized_user)

    class Meta(object):
        model = Album
        fields = ['title', 'description', 'photos']


def frontpage_view(request):
    """View the front page of the website.
    Displays welcome text and links that prompt the user to either login
    or register.
    """
    return render(request, 'PhotoManager/frontpage.html')


@login_required
def home_view(request):
    """View the home page.
    Shows a list of the user's albums with title and description.
    """
    albums = Album.objects.\
        filter(author__exact=request.user.pk).order_by('-date_created')
    context = {'albums': albums}
    return render(request, 'PhotoManager/homepage.html', context)


@login_required
def album_view(request, id):
    """View a single album.
    Shows thumbnails of the photos in the album, plus the album's title
    and description, if any.
    """
    # import pdb; pdb.set_trace()
    album = Album.objects.get(pk=id)
    if album.author.pk != request.user.pk:
        return HttpResponseForbidden("403 Forbidden")
    context = {'album': album}
    return render(request, 'PhotoManager/album.html', context)


@login_required
def photo_view(request, id):
    """View a single photo.
    Shows the photo, its description (if any), and its tags (if any),
    and allow the user the opportunity to add new tags, including the
    ability to create a completely new tag. A POST to this page signifies
    that the user is adding a tag to this photo.
    """
    photo = Photo.objects.get(pk=id)
    if photo.author.pk != request.user.pk:
        return HttpResponseForbidden("403 Forbidden")
    context = {'photo': photo}
    return render(request, 'PhotoManager/photo.html', context)


@login_required
def tag_view(request, id):
    """View a list of photos represented by a certain tag.
    Shows thumbnails of the photos with a certain tag applied, which link
    to that photo's page.
    """
    tag = Tag.objects.get(id=id)
    photos = Photo.objects.filter(author__exact=request.user, tags__id=id)
    context = {'photos': photos, 'tag': tag}
    return render(request, 'PhotoManager/tag.html', context)


@login_required
def create_album_view(request):
    """View that allows users to create an album.
    Presents the user with a form allowing them to initialize album
    details.
    """
    if request.method == 'POST':
        form = AlbumForm(request.POST, authorized_user=request.user)
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
        form = AlbumForm(authorized_user=request.user)

    context = {'form': form}
    return render(request, 'PhotoManager/create_album.html', context)


@login_required
def modify_album_view(request, id):
    """View that allows users to modify an album.
    Presents the user with a form allowing them to change the title or
    description or add or remove photos.
    """
    album = Album.objects.get(pk=id)
    if album.author.pk != request.user.pk:
        return HttpResponseForbidden("403 Forbidden")

    if request.method == 'POST':
        form = AlbumForm(
            request.POST, instance=album, authorized_user=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('PhotoManager:pm-album', args=[album.pk]))

    else:
        form = AlbumForm(instance=album, authorized_user=request.user)

    photo_form = CreatePhotoForm()
    context = {'form': form, 'album': album, 'photo_form': photo_form}
    return render(request, 'PhotoManager/modify_album.html', context)


@login_required
def create_photo_view(request):
    """View that allows the user to create a new photo."""
    if request.method == 'POST':
        album = Album.objects.get(pk=request.POST['album'])
        if album.author.pk != request.user.pk:
            return HttpResponseForbidden("403 Forbidden")

        form = CreatePhotoForm(request.POST, request.FILES)
        if form.is_valid():
            new_photo = form.save(commit=False)
            new_photo.author = request.user
            new_photo.save()
            album.photos.add(new_photo)
            album.save()

        return HttpResponseRedirect(
            reverse('PhotoManager:pm-modify_album', args=[album.pk]))

    else:
        return HttpResponseNotAllowed(
            ['POST'], content='405 Method Not Allowed')


@login_required
def modify_photo_view(request, id):
    """View that allows the user to modify a photo."""
    photo = Photo.objects.get(pk=id)
    if photo.author.pk != request.user.pk:
        return HttpResponseForbidden("403 Forbidden")

    if request.method == 'POST':
        form = EditPhotoForm(request.POST, instance=photo)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('PhotoManager:pm-photo', args=[photo.pk]))

    else:
        form = EditPhotoForm(instance=photo)
        tag_form = TagForm()

    context = {'form': form, 'tag_form': tag_form, 'photo': photo}
    return render(request, 'PhotoManager/modify_photo.html', context)


@login_required
def create_tag_view(request):
    """View that allows the user to create a new tag.
    This view is only reachable from the modify photo view, and so redirects
    there.
    """
    if request.method == 'POST':
        photo = Photo.objects.get(pk=request.POST['photo'])
        if photo.author.pk != request.user.pk:
            return HttpResponseForbidden("403 Forbidden")

        form = TagForm(request.POST)
        if form.is_valid():
            new_tag = form.save()
            photo.tags.add(new_tag)
            photo.save()

        return HttpResponseRedirect(
            reverse('PhotoManager:pm-modify_photo', kwargs={'id': photo.pk}))
    else:
        return HttpResponseNotAllowed(
            ['POST'], content='405 Method Not Allowed')
