# from django.conf.urls import patterns, include, url
from django.conf.urls import *
# from django.views.generic.simple import direct_to_template
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
admin.autodiscover()

from reader import views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'informed.views.home', name='home'),
    # url(r'^informed/', include('informed.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', 'reader.views.home', name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('userena.urls')),
    url(r'^topic/starred/', 'reader.views.display_starred_articles'),
    url(r'^topic/(?P<topic>.*)$', 'reader.views.reader'),
    url(r'^manage-feeds/', 'reader.views.manage_feeds', name='manage-feeds'),
    url(r'^delete-feeds/(?P<id>.*)$', 'reader.views.delete_feed', name='manage-feeds'),
    # not a public-facing URL. Going to this url runs script that parses feeds and adds new articles to db. cron hits url every hour
    url(r'^run-get-new-articles/(?P<id>.*)$', 'reader.views.run_get_new_articles', name='run-get-new-articles'),
    url(r'^star-article/(?P<id>.*)$', 'reader.views.star_article', name='star_article'),
    url(r'^signup_unavail/', 'reader.views.signup_unavail'),
)

urlpatterns += staticfiles_urlpatterns()
