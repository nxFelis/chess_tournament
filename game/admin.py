from .models import Round, Game, Total
from django.contrib import admin


class RoundAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Round',          {'fields': ['title', 'start', 'report', 'couples', 'total', 'active']}),
#        ('Round',          {'fields': ['title', 'report', 'image', 'couples']}),
        ('Gamers',{'fields': ['winners', 'draws', 'losers'], 'classes': ['collapse']}),
        ]

admin.site.register(Round, RoundAdmin)


class GameAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Game',    {'fields': ['title', 'start', 'round', 'black_player', 'white_player', 'result']}),
        ('Details', {'fields': ['btime_limit', 'wtime_limit', 'steps'], 'classes': ['collapse']}),
        ]

admin.site.register(Game, GameAdmin)


class TotalAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Total',    {'fields': ['title', 'addition_coefficients', 'time_rule', 'category']}),
        ('Details',    {'fields': ['players']}),
        ]

admin.site.register(Total, TotalAdmin)
