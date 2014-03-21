from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'PhotoManager.views',
    url(r'^$', 'frontpage_view', name='pm-front'),
    url(r'^home/$', 'home_view', name='pm-home'),
    url(r'^album/(?P<id>\d+)$', 'album_view', name='pm-album'),
    url(r'^photo/(?P<id>\d+)$', 'photo_view', name='pm-photo'),
    url(r'^tag/(?P<id>\d+)$', 'tag_view', name='pm-tag'),
    url(r'^login/$', 'login_view', name='pm-login'),
    url(r'^logout/$', 'logout_view', name='pm-logout'),
)
