from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'PhotoManager.views',
    url(r'^$', 'frontpage_view', name='pm-front'),
    url(r'^home/$', 'home_view', name='pm-home'),
    url(r'^album/(?P<id>\d+)$', 'album_view', name='pm-album'),
    url(r'^album/create$', 'create_album_view', name='pm-create_album'),
    url(r'^album/modify/(?P<id>\d+)$', 'modify_album_view', name='pm-modify_album'),
    url(r'^photo/(?P<id>\d+)$', 'photo_view', name='pm-photo'),
    url(r'^photo/create$', 'create_photo_view', name='pm-create_photo'),
    url(r'^photo/modify/(?P<id>\d+)$', 'modify_photo_view', name='pm-modify_photo'),
    url(r'^tag/(?P<id>\d+)$', 'tag_view', name='pm-tag'),
    url(r'^tag/create$', 'create_tag_view', name='pm-create_tag'),
)
