# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from .models import Player


class PlayerForm(ModelForm):
    playername = forms.SlugField(label=_(u"Имя участника турнира"), required=True,
        max_length=256, help_text=_(u"Необходимое поле. 1-256 символов. Буквы, цифры и знаки пунктуации"),
        error_messages={
            'invalid': _(u"Имя участника турнира может содержать только буквы, цифры и знаки пунктуации."),
            'max_length': _(u"Длина имени участника турнира должна быть 1-256 символов.")
        })
    birth_date = forms.DateField(input_formats=['%d.%m.%Y', ], label=_(u"Дата рождения"),
        help_text=_(u"Необходимое поле."), required=True,
        error_messages={'invalid': _(u"Дата должна быть в формате ДД.ММ.ГГГГ")
    })
    class Meta:
        model = Player
        fields = ('playername', 'birth_date', 'rate', 'country', 'sex', )
