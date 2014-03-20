from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'PhotoManager.views',
    url(r'^$', 'frontpage_view', name='frontpage'),
    url(r'^home/$', 'home_view', name='home'),
    url(r'^album/(?P<id>\d+)$', 'album_view', name='album'),
    url(r'^photo/(?P<id>\d+)$', 'photo_view', name='photo'),
    url(r'^tag/(?P<id>\d+)$', 'tag_view', name='tag'),
    url(r'^login/$', 'login_view', name='login'),
    url(r'^logout/$', 'logout_view', name='logout'),
)
