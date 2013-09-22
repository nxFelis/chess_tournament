# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from .models import Game, RESULT_CHOICES


class ResultForm(ModelForm):
    result = forms.ChoiceField(label=_(u"Результат игры"), required=True,
        choices=RESULT_CHOICES,
        help_text=_(u"Необходимое поле."),
        error_messages={
            'invalid': _(u"Необходимо выбрать результат игры"),
        })
    class Meta:
        model = Game
        fields = ('result', )
