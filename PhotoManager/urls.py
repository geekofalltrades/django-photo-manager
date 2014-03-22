from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'PhotoManager.views',
    url(r'^$', 'frontpage_view', name='pm-front'),
    url(r'^home/$', 'home_view', name='pm-home'),
    url(r'^album/(?P<id>\d+)$', 'album_view', name='pm-album'),
    url(r'^photo/(?P<id>\d+)$', 'photo_view', name='pm-photo'),
    url(r'^tag/(?P<id>\d+)$', 'tag_view', name='pm-tag'),
    url(r'^create/$', 'create_album_view', name='pm-create'),
    url(r'^modify/(?P<id>\d+)$', 'modify_view', name='pm-modify'),
)
