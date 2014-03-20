from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'PhotoManager.views',
    url(r'^$', 'PhotoApp.views.frontpage_view', name='frontpage'),
    url(r'^home/$', 'PhotoApp.views.home_view', name='home'),
    url(r'^album/(?P<id>\d+)$', 'PhotoApp.views.album_view', name='album'),
    url(r'^photo/(?P<id>\d+)$', 'PhotoApp.views.photo_view', name='photo'),
    url(r'^tag/(?P<id>\d+)$', 'PhotoApp.views.tag_view', name='tag'),
    url(r'^login/$', 'PhotoApp.views.login_view', name='login'),
    url(r'^logout/$', 'PhotoApp.views.logout_view', name='logout'),
)
