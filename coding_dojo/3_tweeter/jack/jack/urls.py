from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'jack.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^jack/', include('djack.urls')),
    # url(r'^jack/create/$', 'djack.views.create'),
    url(r'^admin/', include(admin.site.urls)),
)
