# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.http import urlquote

from django.contrib.auth.models import BaseUserManager
import warnings

from core.models import BaseModel, BaseActive, SEX_CHOICES
from chess_test.utils import get_elo_coefficient, get_degree

COUNTRY_CHOICES = (
    (0, 'Don`t know'),
    (1, 'RU'),
    (2, 'UKR'),
    (3, 'USA'),
    )

DEGREE_CHOICES = (
    (0, 'New'),
    (1, 'CM'),
    (2, 'FM'),
    (3, 'IM'),
    (4, 'GM'),
    (5, 'CM'),
    (6, 'WFM'),
    (7, 'WIM'),
    (8, 'WGM')
    )

STATE_CHOICES = (
    (0, 'Don`t know'),
    (1, 'winner'),
    (2, 'draw'),
    (3, 'loser')
    )


class PlayerManager(models.Manager):
    def create_player(self, name, birth_date, country, rate, sex, **extra_fields):
        if not name:
            raise ValueError('We need a player name to create a new chess player')
        player = self.model(playername=name, birth_date=birth_date,
            rate=rate, sex=sex, **extra_fields)
        #TODO: add watcher(bool) & email to invite chess players and extend their abilities
        player.set_password('chess')
        player.is_active = True
        player.save(using=self._db)
        return player


class Player(BaseActive, BaseModel):
    playername = models.CharField(_(u'Имя игрока'), max_length=30, db_index=True)
    birth_date = models.DateField(_(u'День рождения'), blank=True)
    sex = models.IntegerField(_(u'Пол'), choices=SEX_CHOICES, default=0)
    country = models.IntegerField(_(u'Страна'), choices=COUNTRY_CHOICES, default=0)
    rate = models.IntegerField(_(u'Рейтинг'), default=50, blank=True, db_index=True)
    coefficientK = models.IntegerField(_(u'Коэффициент рейтинга Эло'), default=0, blank=True)
    result = models.FloatField(_(u'Счет за турнир'), default=0.0, blank=True)
    place = models.IntegerField(_(u'Место в турнире'), default=0, blank=True)
    degree = models.IntegerField(_(u'Разряд'), choices=DEGREE_CHOICES, default=0)
    is_self_player = models.BooleanField(_(u'Играл без пары?'), default=False)
    state = models.IntegerField(_(u'Состояние после игры'), choices=STATE_CHOICES, default=0)
    color_list = models.CharField(_(u'Цвета фигур'), max_length=4, default='w')

    objects = PlayerManager()

    class Meta:
        verbose_name = _(u'Участник турнира')
        verbose_name_plural = _(u'Участники турнира')
        unique_together = ("playername", "birth_date")
        get_latest_by = "rate"
        ordering = ('created',)

    def get_full_name(self):
        return self.playername

    def get_short_name(self):
        return self.playername

    def __unicode__(self):
        return self.playername

    def is_selfplayer(self):
        return self.is_self_player

    def save(self, *args, **kwargs):
        if self.rate and not self.coefficientK:
            self.coefficientK = get_elo_coefficient(int(self.rate))
        if self.rate:
            self.degree = get_degree(int(self.rate), int(self.sex))
        super(Player, self).save(*args, **kwargs)


class EloManager(models.Manager):
    def change_elo(self, player, **kwargs):
        if not player:
            raise ValueError('We need a player to create a new chess player Elo changing')
        elo = Elo.objects.get(player=player)
        if elo.player and elo.contestants.all():
            elo.waiting_count = 1 / (1 + 10**((int(elo.contestants.all().distinct()[0].rate) - int(elo.player.rate))/400))
            elo.save(update_fields=['waiting_count'], using=self._db)
        if elo.player and elo.real_count and elo.contestants.all():
            elo.player.rate = elo.player.rate + elo.player.coefficientK * (int(elo.real_count) - int(elo.waiting_count))
            elo.player.save(update_fields=['rate'])
        return elo


class Elo(models.Model):
    player = models.OneToOneField(Player)
    waiting_count = models.IntegerField(default=0, blank=True)
    real_count = models.IntegerField(default=0, blank=True)
    contestants = models.ManyToManyField(Player, blank=True, related_name='contestants')
    start_elo = models.IntegerField(default=0, blank=True)

    objects = EloManager()

    class Meta:
        verbose_name = _(u'Рейтинг Эло')
        verbose_name_plural = _(u'Рейтинги Эло')

    def save(self, *args, **kwargs):
        super(Elo, self).save(*args, **kwargs)
        if (not self.start_elo or int(self.start_elo) == 0) and self.player:
            self.start_elo = self.player.rate
            super(Elo, self).save(update_fields=['start_elo'], *args, **kwargs)
        if self.player and self.player.is_self_player:
            self.waiting_count = 1
            super(Elo, self).save(update_fields=['waiting_count'], *args, **kwargs)
