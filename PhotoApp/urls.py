from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'PhotoApp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^pm/', include('PhotoManager.urls', namespace='PhotoManager')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('registration.backends.default.urls'),
        namespace='account'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
