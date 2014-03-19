from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import datetime
from models import Tag, Photo, Album


class TestTagModel(TestCase):
    """Test the tag model of the PhotoManager."""
    def test_create_tag(self):
        """Create a tag and assert that its fields appear as expected."""
        tag = Tag(text='Test Tag')
        tag.full_clean()
        tag.save()
        tag = Tag.objects.get(id=1)
        self.assertIsInstance(tag, Tag)
        self.assertEqual(tag.text, 'Test Tag')
        self.assertIsInstance(tag.timestamp, datetime)

    def test_create_tag_without_text(self):
        """Try to create a tag with no text and assert that the operation
        fails.
        """
        tag = Tag()
        self.assertRaises(ValidationError, tag.full_clean)


class TestPhotoModel(TestCase):
    """Test the photo model of the PhotoManager."""
    def test_create_photo(self):
        """Create a photo and assert that its fields appear as expected."""



class TestAlbumModel(TestCase):
    """Test the album model of the PhotoManager."""
