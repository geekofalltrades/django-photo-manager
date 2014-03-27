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
    fixtures = ['test_auth.json', 'test_photo_manager.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username='django', password='djangopass')
        self.url = "/pm/home/"
        self.login_redirect = "/account/login/?next={}".format(self.url)

    def test_home_page_view(self):
        """Test that the home page appears as it should. Eventually these
        tests will expand to cover changes made when authentication is
        implemented.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('PhotoManager/homepage.html')

    def test_home_view_not_logged_in(self):
        """Try to access the home view when not logged in and assert that
        we are redirected to the login view.
        """
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, self.login_redirect)

    def test_home_view_without_albums(self):
        """Log in as a user with no photos and assert that no photos appear
        on the tag view.
        """
        self.client.logout()
        self.client.login(username='layperson', password='laypass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('class="album"', response.content)

    def test_home_view_with_albums(self):
        """If the logged in user has albums, assert that they appear on
        the front page.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('class="album"', response.content)
        self.assertIn('Test Album', response.content)
        self.assertIn('Test Description', response.content)


class TestTagView(TestCase):
    """Test the tag view.
    The tag view displays a title declaring which tag is represented and
    beneath the title thumbnails of all photos which have that tag, each
    of which links to the photo view for that photo.
    """
    fixtures = ['test_auth.json', 'test_photo_manager.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username='django', password='djangopass')
        self.url = "/pm/tag/{}"
        self.login_redirect = "/account/login/?next={}".format(self.url)

    def test_tag_view(self):
        """Test that the tag view appears as expected."""
        tag = Tag.objects.get(text='dev')
        response = self.client.get(self.url.format(tag.pk))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('PhotoManager/tag.html')

    def test_tag_view_not_logged_in(self):
        """Try to access the tag view when not logged in and assert that
        we are redirected to the login view.
        """
        self.client.logout()
        tag = Tag.objects.get(text='dev')
        response = self.client.get(self.url.format(tag.pk))
        self.assertRedirects(response, self.login_redirect.format(tag.pk))

    def test_tag_view_without_tags(self):
        """Log in as a user with no photos and assert that no photos appear
        on the tag view.
        """
        self.client.logout()
        self.client.login(username='layperson', password='laypass')
        tag = Tag.objects.get(text='dev')
        response = self.client.get(self.url.format(tag.pk))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('img', response.content)

    def test_tag_with_photos(self):
        """Log in as a user with photos and assert that photos with the
        given tag appear on the tag view. Test that thumbnails for every
        photo with this tag appear on the tag view page.
        """
        tag = Tag.objects.get(text='dev')
        response = self.client.get(self.url.format(tag.pk))
        self.assertEqual(response.status_code, 200)
        self.assertIn('img', response.content)
        #assertInHTML does not recognize response.content as HTML even
        #though it most definitely is HTML. It would be useful here because
        #I could assert that every photo with the tag appeared using the
        #"count" keyword argument.


class TestAlbumView(TestCase):
    """Test the album view.
    The album view displays the title of the album, its description, and
    thumbnails of all photos in the album.
    """
    fixtures = ['test_auth.json', 'test_photo_manager.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username='django', password='djangopass')
        self.url = "/pm/album/{}"
        self.login_redirect = "/account/login/?next={}".format(self.url)

    def test_album_view(self):
        """Test that the album view appears as expected."""
        album = Album.objects.get(title="Test Album")
        response = self.client.get(self.url.format(album.pk))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('PhotoManager/album.html')

    def test_album_view_not_logged_in(self):
        """Try to access the album view when not logged in and assert that
        we are redirected to the login view.
        """
        self.client.logout()
        album = Album.objects.get(title="Test Album")
        response = self.client.get(self.url.format(album.pk))
        self.assertRedirects(response, self.login_redirect.format(album.pk))

    def test_album_view_wrong_user(self):
        """Attempt to access an album from a user account that the album
        doesn't belong to.
        """
        self.client.logout()
        self.client.login(username='layperson', password='laypass')
        album = Album.objects.get(title="Test Album")
        response = self.client.get(self.url.format(album.pk))
        self.assertEqual(response.status_code, 403)
        self.assertIn('403 Forbidden', response.content)

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
    fixtures = ['test_auth.json', 'test_photo_manager.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username='django', password='djangopass')
        self.photo = Photo.objects.get(pk=2)
        self.url = "/pm/photo/{}".format(self.photo.pk)
        self.login_redirect = "/account/login/?next={}".format(self.url)

    def test_photo_view(self):
        """Test that the photo view appears as expected."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('PhotoManager/photo.html')

    def test_photo_view_not_logged_in(self):
        """Try to access the photo view when not logged in and assert that
        we are redirected to the login view.
        """
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, self.login_redirect)

    def test_photo_view_wrong_user(self):
        """Attempt to access a photo from a user account that the photo
        doesn't belong to.
        """
        self.client.logout()
        self.client.login(username='layperson', password='laypass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)
        self.assertIn('403 Forbidden', response.content)

    def test_photo_view_elements(self):
        """Assert that the photo and its description and tags appear
        on the photo page.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.photo.image.url, response.content)
        self.assertIn('Description:', response.content)
        self.assertIn(self.photo.description, response.content)
        self.assertIn('Tags:', response.content)
        for tag in self.photo.tags.all():
            self.assertIn(tag.text, response.content)
        self.assertIn('Albums Containing This Photo:', response.content)
        for album in self.photo.album_set.all():
            self.assertIn(album.title, response.content)
        self.assertIn('Edit This Photo', response.content)
        self.assertIn('Return Home', response.content)


class TestCreateAlbumView(TestCase):
    """Test the create album view."""
    fixtures = ['test_auth.json', 'test_photo_manager.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username='django', password='djangopass')
        self.url = "/pm/album/create"
        self.login_redirect = "/account/login/?next={}".format(self.url)

    def test_create_album_view_get(self):
        """Send a GET request to the create album view and insure that the
        page is rendered as expected.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('PhotoManager/create_album.html')

    def test_create_album_view_not_logged_in(self):
        """Try to access the create album view when not logged in and
        assert that we are redirected to the login view.
        """
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, self.login_redirect)

    def test_create_album_view_elements(self):
        """Assert that the required elements are present on the album
        creation page.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Create Album', response.content)
        self.assertIn('Return Home', response.content)
        self.assertIn('Title:', response.content)
        self.assertIn('Description:', response.content)
        self.assertIn('Photos:', response.content)

    def test_create_album(self):
        """Create a new album and assert that that album exists and is
        redirected to.
        """
        form_data = {
            'title': 'Real-Time Test Album',
            'description': 'Real-Time Test Description',
        }
        response = self.client.post(self.url, form_data, follow=True)
        self.assertIn(form_data['title'], response.content)
        self.assertIn(form_data['description'], response.content)

    def test_create_album_missing_title(self):
        """Create an album that's missing a title and assert that the
        operation fails.
        """
        form_data = {
            'title': '',
            'description': 'Real-Time Test Description',
        }
        response = self.client.post(self.url, form_data)
        self.assertTemplateUsed('PhotoManager/create_album.html')
        self.assertIn(form_data['description'], response.content)


class TestModifyAlbumView(TestCase):
    """Test the modify album view."""
    fixtures = ['test_auth.json', 'test_photo_manager.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username='django', password='djangopass')
        self.album = Album.objects.get(title='Test Album')
        self.url = "/pm/album/modify/{}".format(self.album.pk)
        self.redirect = "/pm/album/{}".format(self.album.pk)
        self.login_redirect = "/account/login/?next={}".format(self.url)

    def test_modify_album_view_get(self):
        """Send a GET request to the album modification view and assert
        that it appears as expected.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('PhotoManager/modify_album.html')

    def test_modify_album_view_not_logged_in(self):
        """Try to access the modify album view when not logged in and
        assert that we are redirected to the login view.
        """
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, self.login_redirect)

    def test_modify_album_view_wrong_user(self):
        """Attempt to modify an album from a user account that the album
        doesn't belong to.
        """
        self.client.logout()
        self.client.login(username='layperson', password='laypass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)
        self.assertIn('403 Forbidden', response.content)

    def test_modify_album_view_elements(self):
        """Assert that the required elements are present on the album
        modification page.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Edit Album', response.content)
        self.assertIn('Return Home', response.content)
        self.assertIn('Return to Album', response.content)
        self.assertIn('Title:', response.content)
        self.assertIn('Description:', response.content)
        self.assertIn('Photos:', response.content)
        self.assertIn(self.album.title, response.content)
        self.assertIn(self.album.description, response.content)

    def test_modify_album_view_post(self):
        """Modify some details of an existing album and assert that the
        changes take effect.
        """
        form_data = {
            'title': 'New Test Title',
            'description': 'New Test Description'
        }
        response = self.client.post(self.url, form_data, follow=True)
        self.assertRedirects(response, self.redirect, target_status_code=200)
        self.assertIn(form_data['title'], response.content)
        self.assertIn(form_data['description'], response.content)

    def test_modify_album_view_unallowed_modification(self):
        """Attempt to delete the title of an album and assert that the
        operation fails.
        """
        form_data = {
            'title': '',
            'description': 'New Test Description'
        }
        response = self.client.post(self.url, form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('PhotoManager/modify_album.html')
        self.assertIn(form_data['title'], response.content)
        self.assertIn(form_data['description'], response.content)


class TestCreatePhotoView(TestCase):
    """Test the create photo view."""
    fixtures = ['test_auth.json', 'test_photo_manager.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username='django', password='djangopass')
        self.url = "/pm/photo/create"
        self.login_redirect = "/account/login/?next={}".format(self.url)

    def test_create_photo_view_get(self):
        """Send a GET request to the create photo view and insure that the
        page is rendered as expected.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('PhotoManager/create_photo.html')

    def test_create_photo_view_not_logged_in(self):
        """Try to access the create photo view when not logged in and
        assert that we are redirected to the login view.
        """
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, self.login_redirect)

    def test_create_photo_view_elements(self):
        """Assert that the required elements are present on the photo
        creation page.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Create Photo', response.content)
        self.assertIn('Return Home', response.content)
        self.assertIn('Description:', response.content)
        self.assertIn('Tags:', response.content)
        self.assertIn('Image:', response.content)

    def test_create_photo(self):
        """Create a new photo and assert that that photo exists and is
        redirected to.
        """
        form_data = {
            'description': 'Real-Time Test Photo',
            'image': File(open('test_image.jpg')),
        }
        response = self.client.post(self.url, form_data, follow=True)
        self.assertIn('img', response.content)
        self.assertIn(form_data['description'], response.content)

    def test_create_photo_missing_image(self):
        """Create an photo that's missing an image and assert that the
        operation fails.
        """
        form_data = {
            'description': 'Real-Time Test Photo',
            'image': '',
        }
        response = self.client.post(self.url, form_data)
        self.assertTemplateUsed('PhotoManager/create_photo.html')
        self.assertIn(form_data['description'], response.content)


class TestModifyPhotoView(TestCase):
    """Test the modify photo view."""
    fixtures = ['test_auth.json', 'test_photo_manager.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username='django', password='djangopass')
        self.photo = Photo.objects.get(description='babby')
        self.url = "/pm/photo/modify/{}".format(self.photo.pk)
        self.redirect = "/pm/photo/{}".format(self.photo.pk)
        self.login_redirect = "/account/login/?next={}".format(self.url)

    def test_modify_photo_view_get(self):
        """Send a GET request to the photo modification view and assert
        that it appears as expected.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('PhotoManager/modify_album.html')

    def test_modify_photo_view_not_logged_in(self):
        """Try to access the modify photo view when not logged in and
        assert that we are redirected to the login view.
        """
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, self.login_redirect)

    def test_modify_photo_view_wrong_user(self):
        """Attempt to modify a photo from a user account that the photo
        doesn't belong to.
        """
        self.client.logout()
        self.client.login(username='layperson', password='laypass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)
        self.assertIn('403 Forbidden', response.content)

    def test_modify_photo_view_elements(self):
        """Assert that the required elements are present on the photo
        modification page.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Edit Photo', response.content)
        self.assertIn('Return Home', response.content)
        self.assertIn('Return to Photo', response.content)
        self.assertIn('Description:', response.content)
        self.assertIn('Tags:', response.content)
        self.assertIn('Or, create a new tag for this photo', response.content)
        self.assertIn('Text:', response.content)
        self.assertIn(self.photo.description, response.content)
        for tag in self.photo.tags.all():
            self.assertIn(tag.text, response.content)

    # def test_modify_photo_view_post(self):
    #     """Modify some details of an existing photo and assert that the
    #     changes take effect.
    #     """
    #     form_data = {
    #         'description': 'New Test Description',
    #         'tags': '????????????????????????????????????????????????????????',
    #     }
    #     response = self.client.post(self.url, form_data, follow=True)
    #     self.assertRedirects(response, self.redirect, target_status_code=200)
    #     self.assertIn(form_data['title'], response.content)
    #     self.assertIn(form_data['description'], response.content)


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
