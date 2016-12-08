from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'writersinthecloud.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^rain/', include('rain.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
