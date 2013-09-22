from .models import Player, Elo
from django.contrib import admin

class EloInline(admin.TabularInline):
    model = Elo
    extra = 1

class PlayerAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Player',          {'fields': ['playername', 'birth_date', 'rate', 'sex', 'country']}),
        ('Details',         {'fields': ['degree', 'coefficientK'], 'classes': ['collapse']}),
        ('Game information',{'fields': ['result', 'place', 'is_self_player', 'state', 'color_list'], 'classes': ['collapse']}),
        ]
    inlines = [EloInline]

admin.site.register(Player, PlayerAdmin)
