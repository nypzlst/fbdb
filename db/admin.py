from django.contrib import admin
from .models import FbFederation, FbSeason,FbSubtitution,FbCompetition, FbCountry, FbLeague, FbTeam, FbStandings, FbGoal,FbMatch,FbPlayer,FbIncedent

# Register your models here.
admin.site.register(FbFederation)
admin.site.register(FbCompetition)
admin.site.register(FbCountry)
admin.site.register(FbLeague)
admin.site.register(FbTeam)
admin.site.register(FbStandings)
admin.site.register(FbSeason)
admin.site.register(FbMatch)
admin.site.register(FbPlayer)
admin.site.register(FbIncedent)

admin.site.register(FbGoal)
admin.site.register(FbSubtitution)
# admin.site.register()
# admin.site.register()
# admin.site.register()
# admin.site.register()
# admin.site.register()
# admin.site.register()
