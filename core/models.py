# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

SEX_CHOICES = (
    (0, 'Don`t know'),
    (1, 'Male'),
    (2, 'Female')
    )


class BaseModel(models.Model):
    created = models.DateTimeField(verbose_name=_(u'Created data and time'),
        auto_now_add=True)

    class Meta:
        abstract = True


class BaseActive(models.Model):
    active = models.BooleanField(default=True)

    class Meta(object):
        abstract = True

    def is_active(self):
        return self.active


class BaseTitle(models.Model):
    title = models.CharField(_(u'Название'), max_length=256)

    class Meta:
        abstract = True
