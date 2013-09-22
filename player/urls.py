from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from player import views
from player.views import PlayerListView, PlayerView

urlpatterns = patterns('',
#    url(r'^$', views.index, name='player_index'),
    url(r'^$', PlayerListView.as_view(), name='player'),
    url(r'^add_player/', views.add_player, name='player-add'),
    url(r'^(?P<pk>\d+)/$', PlayerView.as_view(), name='player-detail'),

)