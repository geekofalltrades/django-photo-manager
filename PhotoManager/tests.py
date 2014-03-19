from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from datetime import datetime
from models import Tag, Photo, Album


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

    def test_create_photo(self):
        """Create a photo and assert that its fields appear as expected."""
        photo = Photo(
            author=self.u,
            description='A Photo',

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
        photo = Photo()
        self.assertRaises(ValidationError, photo.full_clean)

    def test_create_photo_without_image(self):
        """Attempt to create a photo without an image and verify that
        the operation raises a ValidationError.
        """
        photo = Photo()
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

        photo = Photo(author=self.u)
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
