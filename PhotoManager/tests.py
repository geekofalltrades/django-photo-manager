from django.test import TestCase
from django.test.client import Client
from django.core.exceptions import ValidationError
from django.core.files import File
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime
from models import Tag, Photo, Album
from shutil import rmtree
import os


class TestTagModel(TestCase):
    """Test the tag model of the PhotoManager."""
    def test_create_tag(self):
        """Create a tag and assert that its fields appear as expected."""
        tag = Tag(text='Test Tag')
        tag.full_clean()
        tag.save()
        self.assertIsInstance(tag, Tag)
        self.assertEqual(tag.text, 'Test Tag')
        self.assertIsInstance(tag.date_created, datetime)

    def test_create_tag_without_text(self):
        """Try to create a tag with no text and assert that the operation
        fails.
        """
        tag = Tag()
        self.assertRaises(ValidationError, tag.full_clean)


class TestPhotoModel(TestCase):
    """Test the photo model of the PhotoManager."""
    def setUp(self):
        self.u = User(username='admin', password='password')
        self.u.save()
        self.image = File(open('test_image.jpg'))

    def tearDown(self):
        """After each test, remove the image file uploaded."""
        rmtree(
            os.path.join(settings.MEDIA_ROOT, str(self.u.pk)),
            ignore_errors=True
        )

    def test_create_photo(self):
        """Create a photo and assert that its fields appear as expected."""
        photo = Photo(
            author=self.u,
            description='A Photo',
            image=self.image
        )
        photo.full_clean()
        photo.save()
        self.assertIsInstance(photo, Photo)
        self.assertIsInstance(photo.date_created, datetime)
        self.assertIsInstance(photo.date_modified, datetime)
        self.assertEqual(photo.description, 'A Photo')
        self.assertEqual(photo.author, self.u)

    def test_create_photo_without_author(self):
        """Attempt to create a photo without an author and verify that
        the operation raises a ValidationError.
        """
        photo = Photo(image=self.image)
        self.assertRaises(ValidationError, photo.full_clean)

    def test_create_photo_without_image(self):
        """Attempt to create a photo without an image and verify that
        the operation raises a ValidationError.
        """
        photo = Photo(author=self.u)
        self.assertRaises(ValidationError, photo.full_clean)

    def test_create_photo_with_tags(self):
        """Create a photo with several tags and assert that they appear
        as expected.
        """
        t1 = Tag(text="Tag 1")
        t1.save()
        t2 = Tag(text="Tag 2")
        t2.save()
        t3 = Tag(text="Tag 3")
        t3.save()

        photo = Photo(author=self.u, image=self.image)
        photo.save()
        photo.tags.add(t1, t2, t3)
        photo.save()

        self.assertIn(t1, photo.tags.all())
        self.assertIn(t2, photo.tags.all())
        self.assertIn(t3, photo.tags.all())


class TestAlbumModel(TestCase):
    """Test the album model of the PhotoManager."""
    def setUp(self):
        self.u = User(username='admin', password='password')
        self.u.save()

    def test_create_album(self):
        """Create an album and verify that it appears as expected."""
        album = Album(
            title='An Album',
            description='A Description',
            author=self.u
        )
        album.full_clean()
        album.save()
        self.assertIsInstance(album, Album)
        self.assertIsInstance(album.date_created, datetime)
        self.assertIsInstance(album.date_modified, datetime)
        self.assertEqual(album.title, 'An Album')
        self.assertEqual(album.description, 'A Description')
        self.assertEqual(album.author, self.u)

    def test_create_album_without_title(self):
        """Attempt to create an album without a title and verify that
        it raises a ValidationError.
        """
        album = Album(author=self.u)
        self.assertRaises(ValidationError, album.full_clean)

    def test_create_album_without_author(self):
        """Attempt to create an album without an author and verify that
        it raises a ValidationError.
        """
        album = Album(title='A Title')
        self.assertRaises(ValidationError, album.full_clean)

    def test_create_album_with_photos(self):
        """Create an album containing several photos and assert that they
        appear as expected.
        """
        photo1 = Photo(author=self.u)
        photo1.save()
        photo2 = Photo(author=self.u)
        photo2.save()
        photo3 = Photo(author=self.u)
        photo3.save()

        album = Album(
            title='An Album',
            description='A Description',
            author=self.u
        )
        album.save()
        album.photos.add(photo1, photo2, photo3)
        album.save()

        self.assertIn(photo1, album.photos.all())
        self.assertIn(photo2, album.photos.all())
        self.assertIn(photo3, album.photos.all())


class TestFrontView(TestCase):
    """Test the front page view of the website.
    The front view simply displays a title and slogan and the option to
    log in or register.
    """
    def setUp(self):
        self.client = Client()
        self.url = "/pm/"

    def test_front_page_view(self):
        """Test that the front page appears as it should."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('PhotoManager/frontpage.html')
        self.assertIn('Log In', response.content)
        self.assertIn('Register', response.content)


class TestHomeView(TestCase):
    """Test the homepage view.
    The home page displays the albums belonging to the user who is logged
    in.
    """
    def setUp(self):
        self.client = Client()
        self.url = "/pm/home/"

    def test_home_page_view(self):
        """Test that the home page appears as it should. Eventually these
        tests will expand to cover changes made when authentication is
        implemented.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('PhotoManager/homepage.html')

    def test_home_page_with_albums(self):
        """If the logged in user has albums, assert that they appear on
        the front page.
        """
        self.user = User(username='django', password='djangopass')
        self.user.save()
        self.album = Album(
            author=self.user,
            title='Test Album',
            description='Test Album Description'
        )
        self.album.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Album', response.content)
        self.assertIn('Test Album Description', response.content)

    def test_home_page_without_albums(self):
        """If the logged in user does not have albums, assert that a line
        prompting the user to create one appears on the home page.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("You don't have any albums yet", response.content)


class TestTagView(TestCase):
    """Test the tag view.
    The tag view displays a title declaring which tag is represented and
    beneath the title thumbnails of all photos which have that tag, each
    of which links to the photo view for that photo.
    """
    fixtures = ['test_auth.json', 'test_photo_manager.json']

    def setUp(self):
        self.client = Client()
        self.url = "/pm/tag/{}"

    def test_tag_view(self):
        """Test that the tag view appears as expected."""
        tag = Tag.objects.get(text='dev')
        response = self.client.get(self.url.format(tag.pk))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('PhotoManager/tag.html')

    def test_tag_with_photos(self):
        """Test that thumbnails for every photo with this tag appear on
        the tag view page.
        """
        tag = Tag.objects.get(text='dev')
        response = self.client.get(self.url.format(tag.pk))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('PhotoManager/tag.html')
        self.assertIn('img', response.content)
        #assertInHTML does not recognize response.content as HTML even
        #though it most definitely is HTML. It would be useful here because
        #I could assert that every photo with the tag appeared using the
        #count keyword argument.


class TestAlbumView(TestCase):
    """Test the album view.
    The album view displays the title of the album, its description, and
    thumbnails of all photos in the album.
    """
    fixtures = ['test_auth.json', 'test_photo_manager.json']

    def setUp(self):
        self.client = Client()
        self.url = "/pm/album/{}"

    def test_album_view(self):
        """Test that the album view appears as expected."""
        album = Album.objects.get(title="Test Album")
        response = self.client.get(self.url.format(album.pk))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('PhotoManager/album.html')

    def test_album_view_no_photos(self):
        """Verify that an album containing no photos still displays
        title and description.
        """
        album = Album.objects.get(title="Test Album")
        response = self.client.get(self.url.format(album.pk))
        self.assertEqual(response.status_code, 200)
        self.assertIn(album.title, response.content)
        self.assertIn(album.description, response.content)

    def test_album_view_with_photos(self):
        """Verify that an album containing photos shows title, description,
        and thumbnails.
        """
        album = Album.objects.get(title="Another Test Album")
        response = self.client.get(self.url.format(album.pk))
        self.assertEqual(response.status_code, 200)
        self.assertIn(album.title, response.content)
        self.assertIn(album.description, response.content)
        self.assertIn('preview', response.content)


class TestPhotoView(TestCase):
    """Test the photo view.
    The photo view displays the photo, its description, a list of its
    tags, and a link back to the album that contains it, and a link back
    to the homepage.
    """
    def setUp(self):
        self.client = Client()
        self.user = User(username='django', password='djangopass')
        self.user.save()
        self.album = Album(
            author=self.user,
            title='Test Album',
            description='Test Album Description'
        )
        self.album.save()
        self.photo = Photo(
            image=File(open('test_image.jpg')),
            author=self.user
        )
        self.photo.save()
        self.album.photos.add(self.photo)
        self.album.save()
        self.url = "/pm/photo/%s" % self.photo.pk

    def test_photo_view(self):
        """Test that the photo view appears as expected."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('PhotoManager/photo.html')

    def test_photo_view_elements(self):
        """Assert that the photo and its description and tags appear
        on the photo page.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.photo.image.url, response.content)
        self.assertIn('Description:', response.content)
        self.assertIn('Tags:', response.content)

    def test_tags_on_photo_view(self):
        """Add a tag to the photo and assert that the tag appears on the
        photo view.
        """
        tag_text = "DevelopmentTag"
        tag = Tag(text=tag_text)
        tag.save()
        self.photo.tags.add(tag)
        self.photo.save()
        #import pdb; pdb.set_trace()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(tag_text, response.content)


class TestCreateAlbumView(TestCase):
    """Test the create album view."""
    def setUp(self):
        self.client = Client()
        self.url = "/pm/album/create"
        self.redirect = "pm/album/%s"

    def test_create_album(self):
        """Create a new album and assert that that album exists and is
        redirected to.
        """
        form_data = {
            'title': 'Test Album',
            'description': 'Test Description',
        }
        response = self.client.post(self.url, form_data)
        new_album = Album.objects.get(title=form_data['title'])
        self.assertRedirects(response, self.redirect.format(new_album.pk))
        self.assertIn(form_data['title'], response.content)
        self.assertIn(form_data['description'], response.content)

    def test_create_album_missing_title(self):
        """Create an album that's missing a title and assert that the
        operation fails.
        """
        form_data = {
            'title': '',
            'description': 'Test Description',
        }
        response = self.client.post(self.url, form_data)
        new_album = Album.objects.get(title=form_data['title'])
        self.assertRedirects(response, self.redirect.format(new_album.pk))
        self.assertIn(form_data['title'], response.content)
        self.assertIn(form_data['description'], response.content)


class TestModifyAlbumView(TestCase):
    """Test the modify album view."""
    def setUp(self):
        self.client = Client()
        self.url = "/pm/album/modify"

    def test_modify_album(self):
        """Modify some details of an existing album and assert that the
        changes take effect.
        """

    def test_modify_unallowed(self):
        """Attempt to delete the title of an album and assert that the
        operation fails.
        """


class TestCreatePhotoView(TestCase):
    """Test the create photo view."""
    def setUp(self):
        self.client = Client()
        self.url = "/pm/photo/create"

    def test_create_photo(self):
        """Create a new photo."""

    def test_create_photo_bad_image(self):
        """Attempt to create a photo using an image that doesn't exist and
        assert that the operation fails.
        """

    def test_create_photo_no_image(self):
        """Try to create a photo without an image and assert that the
        operation fails.
        """


class TestModifyPhotoView(TestCase):
    """Test the modify photo view."""
    def setUp(self):
        self.client = Client()
        self.url = "/pm/photo/modify"

    def test_modify_photo(self):
        """Modify a photo and assert that the changes take effect."""


class TestCreateTagView(TestCase):
    """Test the create tag view."""
    def setUp(self):
        self.client = Client()
        self.url = "/pm/tag/create"

    def test_create_tag(self):
        "Create a new tag."

    def test_create_tag_without_text(self):
        """Attempt to create a tag without text and assert that the
        operation fails.
        """
