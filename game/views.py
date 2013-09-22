# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_list_or_404, \
    get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect

from chess_test.utils import set_player_result
from game.models import Game, Round, Total, RESULT_CHOICES
from player.models import Player, Elo
from game.forms import ResultForm

def tournament(request):
    tournaments_list = Total.objects.all().order_by('-created')
    context = {'tournaments_list': tournaments_list,
               'result_choices': RESULT_CHOICES}
    return render(request, 'game/tournament.html', context)


class GameListView(ListView):
    model = Game
    queryset = Game.objects.order_by('-created')
    template_name = "game/games.html"
    context_object_name = 'games_list'


class GameView(DetailView):
    queryset = Game.objects.all()
    template_name = "game/game.html"

    def get_object(self):
        object = super(GameView, self).get_object()
        return object

    def get_context_data(self, **kwargs):
        context = super(GameView, self).get_context_data(**kwargs)
        context['result'] = RESULT_CHOICES[self.object.result][1]
        return context


class RoundListView(ListView):
    model = Round
    queryset = Round.objects.order_by('-created')
    template_name = "game/rounds.html"
    context_object_name = 'rounds_list'

    def get_context_data(self, **kwargs):
        context = super(RoundListView, self).get_context_data(**kwargs)
        no_actives = False if Round.objects.filter(active=True) else True
        context['allow_creation'] = no_actives
        return context


class RoundView(DetailView):
    queryset = Round.objects.all()
    template_name = "game/round.html"

    def get_object(self):
        object = super(RoundView, self).get_object()
        return object

    def get_context_data(self, **kwargs):
        context = super(RoundView, self).get_context_data(**kwargs)
        context['result_choices'] = dict(RESULT_CHOICES)
        return context

@csrf_protect
def edit_game_result(request, pk):
    if request.method == 'POST':
        game = get_object_or_404(Game, pk=pk)
        result_form = ResultForm(request.POST, instance=game)
        if result_form.is_valid():
            result_form.save()
            result = result_form.cleaned_data['result']
            game.black_player.result += set_player_result(result, 'black')
            game.black_player.save(update_fields=['result'])
            game.white_player.result += set_player_result(result, 'white')
            game.white_player.save(update_fields=['result'])
            return redirect('rounds')
        else:
            context = {'status_code': 201}
            context = {'errorlist': _(u'Ошибка во введенных данных')}
            return render_to_response('game/game_result_edit.html', context, context_instance=RequestContext(request))
    else:
        game = get_object_or_404(Game, pk=pk)
        result_form = ResultForm(request.POST, instance=game)
        context = {'title': _(u'Изменить результат игры'),
                   'pk': pk, 'game': game, 'result_form': result_form,}
        return render_to_response('game/game_result_edit.html', context, context_instance=RequestContext(request))

@csrf_protect
def finish_round(request, pk):
    round = get_object_or_404(Round, pk=pk)
    round.active = False
    round.save(update_fields=['active'])
    games = round.game_set.all()
    for game in games:
        black_elo = get_object_or_404(Elo, player=game.black_player)
        Elo.objects.change_elo(game.white_player)
        white_elo = get_object_or_404(Elo, player=game.white_player)
        Elo.objects.change_elo(game.white_player)
    return redirect('rounds')