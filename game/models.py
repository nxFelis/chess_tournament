# -*- coding: utf-8 -*-

from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from chess_test.utils import upload_to_dir, get_limit, \
    get_last_and_group, normalize_group, get_couples_and_selfplayer, \
    get_total_couples, get_waiting_counts
from core.models import BaseModel, BaseActive, BaseTitle
from player.models import Player, Elo

RESULT_CHOICES = (
    (0, 'Game is in process'),
    (1, '0-1'),
    (2, '1-0'),
    (3, '1/2'),
    (4, '+/-'),
    (5, '-/+'),
    (6, '-/-'),
    )

COEFFICIENTS_CHOICES = (
    (0, _(u'Не учитывать')),
    (1, _(u'Коэффициент Бухгольца')),
    (2, _(u'Усеченный коэффициент Бухгольца'))
    )


class Total(BaseActive, BaseModel):
    title = models.CharField(_(u'Название турнира'), max_length=512)
    players = models.ManyToManyField(Player, blank=True)
    time_rule = models.TextField(verbose_name=_(u'Ограничения по времени'), max_length=1024, blank=True, default='')
    category = models.TextField(verbose_name=_(u'Категория турнира'), max_length=1024, blank=True, default='')
    addition_coefficients = models.IntegerField(verbose_name=_(u'Дополнительные коэффициенты'),
        choices=COEFFICIENTS_CHOICES, default=0)
#    couples = models.CharField(_(u'Список еще не игравших'), blank=True, max_length=4096)

    class Meta:
        verbose_name = _(u'Турнир')
        verbose_name_plural = _(u'Турниры')

    def __unicode__(self):
        return self.title

#    def save(self, *args, **kwargs):
#        super(Total, self).save(*args, **kwargs)
#        if self.players.all():
#            group = self.players.all().order_by('rate')
#            waiting_counts = get_waiting_counts(list(group))
#            for i in xrange(len(group)):
#                group[i].elo.waiting_count = waiting_counts[i][1]
#            self.players = group
#        super(Total, self).save(update_fields=['players'], *args, **kwargs)


class Round(BaseActive, BaseModel, BaseTitle):
    total = models.ForeignKey(Total, verbose_name=_(u'Турнир'))
    report = models.CharField(_(u'Репортаж'), max_length=8192)
    start = models.DateField(_(u'День проведения'), blank=True, default=datetime.now())
#    image = models.ImageField(upload_to=upload_to_dir('Image/report'), verbose_name=_(u'Фото репортажа'))
    couples = models.CharField(_(u'Участники'), blank=True, max_length=4096)
    winners = models.ManyToManyField(Player, blank=True, related_name='winner')
    draws = models.ManyToManyField(Player, blank=True, related_name='draw')
    losers = models.ManyToManyField(Player, blank=True, related_name='loser')

    class Meta:
        verbose_name = _(u'Тур')
        verbose_name_plural = _(u'Туры')

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Round, self).save(*args, **kwargs)
        if not self.couples and not self.losers.all():
            players = self.total.players.all()
            group = list(players.order_by('-rate'))
            player, couples_group = normalize_group(group)
            if player:
                player.is_self_player = True
                player.save(update_fields=['is_self_player'])
            _junk, couples = get_couples_and_selfplayer(list(couples_group))
            self.couples = '; '.join([','.join(couple) for couple in couples])
            super(Round, self).save(update_fields=['couples'], *args, **kwargs)
        if not self.couples and self.losers.all():
            rounds = self.total.round_set.all()
            first_couples = rounds.order_by('-created')[0].couples
            couples = first_couples.split(';')
            total_couples = get_total_couples(self.total.players.all())
            allow_couples = [x for x in total_couples if x not in couples]
            winners = self.winners.all()
            draws = self.draws.all()
            losers = self.losers.all()

            selfplayer, win_couples = get_couples_and_selfplayer(winners)
            success_win_couples = [x for x in win_couples if x in allow_couples]
            if len(success_win_couples) == len(win_couples):
                self.couples = success_win_couples
            else:
                winners = self.winners.all().order_by('-created')
                selfplayer, win_couples = get_couples_and_selfplayer(winners)
                success_win_couples = [x for x in win_couples if x in allow_couples]
                self.couples = success_win_couples
            if selfplayer:
                draws = normalize_group(draws, selfplayer)

            selfplayer, draw_couples = get_couples_and_selfplayer(draws)
            success_draw_couples = [x for x in draw_couples if x in allow_couples]
            if len(success_draw_couples) == len(draw_couples):
                self.couples += success_draw_couples
            else:
                draws = self.draws.all().order_by('-created')
                selfplayer, draw_couples = get_couples_and_selfplayer(draws)
                success_draw_couples = [x for x in draw_couples if x in allow_couples]
                self.couples += success_draw_couples
            if selfplayer:
                losers = normalize_group(losers, selfplayer)

            selfplayer, loser_couples = get_couples_and_selfplayer(losers)
            success_loser_couples = [x for x in loser_couples if x in allow_couples]
            if len(success_loser_couples) == len(loser_couples):
                self.couples += success_loser_couples
            else:
                losers = self.losers.all().order_by('-created')
                selfplayer, loser_couples = get_couples_and_selfplayer(losers)
                success_loser_couples = [x for x in loser_couples if x in allow_couples]
                self.couples += success_loser_couples
            if selfplayer:
                selfplayer.is_self_player = True
                selfplayer.save(update_fields=['is_self_player'])
            super(Round, self).save(update_fields=['couples'], *args, **kwargs)


class Game(BaseActive, BaseModel, BaseTitle):
    round = models.ForeignKey(Round, verbose_name=_(u'Тур'))
    start = models.TimeField(_(u'Время начала'), blank=True, default=datetime.now())
    black_player = models.ForeignKey(Player, related_name='black_player')
    white_player = models.ForeignKey(Player, related_name='white_player')
    result = models.IntegerField(_(u'Результат игры'), choices=RESULT_CHOICES, default=0)
    btime_limit = models.TimeField(_(u'Лимит времени для черных'), blank=True, default=get_limit(datetime.now()))
    wtime_limit = models.TimeField(_(u'Лимит времени для белых'), blank=True, default=get_limit(datetime.now()))
    steps = models.TextField(verbose_name=_(u'Запись ходов'), max_length=8196, blank=True, default='')

    class Meta:
        verbose_name = _(u'Игра')
        verbose_name_plural = _(u'Игры')

    def __unicode__(self):
        s = (u'%s в процессе') % self.title if self.result == 0 \
                             else u'%s результат игры %s' % (self.title, RESULT_CHOICES[self.result][1])
        return s
