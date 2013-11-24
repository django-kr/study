from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fizzbuzz.views.home', name='home'),
    url(r'^$', 'fizzbuzz.views.view_for_hg'),
    url(r'^fizz_buzz/', 'munjae.views.fizz_buzz'),

    url(r'^admin/', include(admin.site.urls)),
)
