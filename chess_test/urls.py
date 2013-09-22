from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from game import views

if 'django.contrib.admin' in settings.INSTALLED_APPS:
    admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'chess_test.views.home', name='home'),
    # url(r'^chess_test/', include('chess_test.foo.urls')),
#    url(r'^$', 'chess_test.views.index', name='index'),

#    url(r'^judge/', include('users.urls')),
    url(r'^$', views.tournament, name='tournament'),
    url(r'^game/', include('game.urls')),
    url(r'^player/', include('player.urls')),
)

urlpatterns += staticfiles_urlpatterns()

if 'django.contrib.admin' in settings.INSTALLED_APPS and settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^admin/', include(admin.site.urls)),
    )
