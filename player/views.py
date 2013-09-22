# -*- coding: utf-8 -*-

from django import forms
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect

from player.models import Player
from player.forms import PlayerForm


class PlayerListView(ListView):
    model = Player
    queryset = Player.objects.order_by('-rate')
    template_name = "player/players.html"
    context_object_name = 'players_list'


class PlayerView(DetailView):
    queryset = Player.objects.all()
    template_name = "player/player.html"

    def get_object(self):
        object = super(PlayerView, self).get_object()
        return object


@csrf_protect
def add_player(request):
    if request.method == 'POST':
        player = Player()
        player_form = PlayerForm(request.POST, instance=player)
        if player_form.is_valid():
            player_form.save()
            return redirect('player')
        else:
            context = {'status_code': 201}
            context = {'errorlist': _(u'Ошибка во введенных данных')}
            return render_to_response('player/player_add.html', context, context_instance=RequestContext(request))
    else:
        player_form = PlayerForm()
        context = {'title': _(u'Создание игрока'), 'player_form': player_form}
        return render_to_response('player/player_add.html', context, context_instance=RequestContext(request))
