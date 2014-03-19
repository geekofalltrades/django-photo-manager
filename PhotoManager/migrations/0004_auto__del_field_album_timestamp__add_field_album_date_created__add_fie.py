# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Album.timestamp'
        db.delete_column(u'PhotoManager_album', 'timestamp')

        # Adding field 'Album.date_created'
        db.add_column(u'PhotoManager_album', 'date_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2014, 3, 19, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Album.date_modified'
        db.add_column(u'PhotoManager_album', 'date_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2014, 3, 19, 0, 0), blank=True),
                      keep_default=False)

        # Deleting field 'Photo.timestamp'
        db.delete_column(u'PhotoManager_photo', 'timestamp')

        # Deleting field 'Photo.title'
        db.delete_column(u'PhotoManager_photo', 'title')

        # Adding field 'Photo.image'
        db.add_column(u'PhotoManager_photo', 'image',
                      self.gf('django.db.models.fields.files.ImageField')(default=datetime.datetime(2014, 3, 19, 0, 0), max_length=100),
                      keep_default=False)

        # Adding field 'Photo.date_created'
        db.add_column(u'PhotoManager_photo', 'date_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2014, 3, 19, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Photo.date_modified'
        db.add_column(u'PhotoManager_photo', 'date_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2014, 3, 19, 0, 0), blank=True),
                      keep_default=False)

        # Deleting field 'Tag.timestamp'
        db.delete_column(u'PhotoManager_tag', 'timestamp')

        # Adding field 'Tag.date_created'
        db.add_column(u'PhotoManager_tag', 'date_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2014, 3, 19, 0, 0), blank=True),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Album.timestamp'
        raise RuntimeError("Cannot reverse this migration. 'Album.timestamp' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Album.timestamp'
        db.add_column(u'PhotoManager_album', 'timestamp',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True),
                      keep_default=False)

        # Deleting field 'Album.date_created'
        db.delete_column(u'PhotoManager_album', 'date_created')

        # Deleting field 'Album.date_modified'
        db.delete_column(u'PhotoManager_album', 'date_modified')


        # User chose to not deal with backwards NULL issues for 'Photo.timestamp'
        raise RuntimeError("Cannot reverse this migration. 'Photo.timestamp' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Photo.timestamp'
        db.add_column(u'PhotoManager_photo', 'timestamp',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True),
                      keep_default=False)

        # Adding field 'Photo.title'
        db.add_column(u'PhotoManager_photo', 'title',
                      self.gf('django.db.models.fields.TextField')(default='Untitled', max_length=64),
                      keep_default=False)

        # Deleting field 'Photo.image'
        db.delete_column(u'PhotoManager_photo', 'image')

        # Deleting field 'Photo.date_created'
        db.delete_column(u'PhotoManager_photo', 'date_created')

        # Deleting field 'Photo.date_modified'
        db.delete_column(u'PhotoManager_photo', 'date_modified')


        # User chose to not deal with backwards NULL issues for 'Tag.timestamp'
        raise RuntimeError("Cannot reverse this migration. 'Tag.timestamp' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Tag.timestamp'
        db.add_column(u'PhotoManager_tag', 'timestamp',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True),
                      keep_default=False)

        # Deleting field 'Tag.date_created'
        db.delete_column(u'PhotoManager_tag', 'date_created')


    models = {
        u'PhotoManager.album': {
            'Meta': {'object_name': 'Album'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photos': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['PhotoManager.Photo']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'PhotoManager.photo': {
            'Meta': {'object_name': 'Photo'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['PhotoManager.Tag']", 'null': 'True', 'blank': 'True'})
        },
        u'PhotoManager.tag': {
            'Meta': {'object_name': 'Tag'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['PhotoManager']