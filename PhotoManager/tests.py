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
    def setUp(self):
        self.client = Client()
        self.tag_text = "test_tag"
        self.tag = Tag(text=self.tag_text)
        self.tag.save()
        self.url = "/pm/tag/%s" % self.tag.pk

    def test_tag_view(self):
        """Test that the tag view appears as expected."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('PhotoManager/tag.html')


class TestAlbumView(TestCase):
    """Test the album view.
    The album view displays the title of the album, its description, and
    thumbnails of all photos in the album.
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
        self.url = "/pm/album/%s" % self.album.pk

    def test_album_view(self):
        """Test that the album view appears as expected."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('PhotoManager/album.html')

    def test_album_view_no_photos(self):
        """Verify that an album containing no photos still displays
        title and description.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Album', response.content)
        self.assertIn('Test Album Description', response.content)

    def test_album_view_with_photos(self):
        """Verify that an album containing photos shows title, description,
        and thumbnails.
        """
        self.photo = Photo(
            image=File(open('test_image.jpg')),
            author=self.user
        )
        self.photo.save()
        self.album.photos.add(self.photo)
        self.album.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Album', response.content)
        self.assertIn('Test Album Description', response.content)
        #assert that there's a photo in here


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
