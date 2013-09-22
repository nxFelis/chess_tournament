# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.utils import timezone

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

from core.models import SEX_CHOICES
from chess_test.utils import normalize_email


class CUserManager(BaseUserManager):
    def create_user(self, email, username=None, **kwargs):
        email = normalize_email(email)
        if not email:
            raise ValueError('We need a user email to create a new chess user')
        user = self.model(email=email, **kwargs)
        user.set_password('chess')
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, username=None, **kwargs):
        su = self.create_user(username=username, email=email, password=password, **kwargs)
        su.is_superuser = True
        su.is_staff = True
        su.is_active = True
        su.save(using=self._db)
        return su


class CUser(AbstractBaseUser):
    email = models.EmailField(_(u"Email"), max_length=255, db_index=True, unique=True)
    username = models.CharField(_(u'Логин'), max_length=30, blank=True)
    birth_date = models.DateField(_(u'День рождения'), blank=True, null=True)
    first_name = models.CharField(_(u'Имя'), max_length=30, blank=True)
    last_name = models.CharField(_(u'Фамилия'), max_length=30, blank=True)
    sex = models.IntegerField(_(u'Пол'), choices=SEX_CHOICES, default=0)
    is_staff = models.BooleanField(_(u'Персонал?'), default=True)
    is_active = models.BooleanField(_(u'Активен?'), default=True)
    date_joined = models.DateTimeField(_(u'Дата регистрации'), default=timezone.now)

    objects = CUserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _(u'Судья')
        verbose_name_plural = _(u'Судьи')

    def _get_full_name(self):
        if self.first_name and self.last_name:
            return ' '.join([self.first_name, self.last_name])
        return self.email

    full_name = property(_get_full_name)

    def get_short_name(self):
        if self.username:
            return self.username
        elif self.first_name:
            return self.first_name
        return self.email

    def email_user(self, subject, message, from_email=None, notifier='email'):
        """
        Sends an email to this .
        """
        if notifier and notifier == 'email':
            send_mail(subject, message, from_email, [self.email])

    def __unicode__(self):
        return self.email