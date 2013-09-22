from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from game import views
from game.views import GameListView, GameView, \
    RoundListView, RoundView

urlpatterns = patterns('',
    url(r'^$', views.tournament, name='tournament'),
    url(r'^games/$', GameListView.as_view(), name='games'),
#    (r'^add_game/', login_required(GameView.as_view())),
    url(r'^games/(?P<pk>\d+)/$', GameView.as_view(), name='game-detail'),
    url(r'^games/(?P<pk>\d+)/edit$', views.edit_game_result, name='game-result-edit'),
    url(r'^rounds/$', RoundListView.as_view(), name='rounds'),
#        (r'^add_round/', login_required(RoundView.as_view())),
    url(r'^rounds/(?P<pk>\d+)/$', RoundView.as_view(), name='round-detail'),
    url(r'^rounds/(?P<pk>\d+)/finish$', views.finish_round, name='round-finish'),

)