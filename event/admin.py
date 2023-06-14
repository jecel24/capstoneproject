from django.contrib import admin
from .models import Team, Player, Game, Score, Standings, Notice

admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Game)
admin.site.register(Score)
admin.site.register(Standings)
admin.site.register(Notice)