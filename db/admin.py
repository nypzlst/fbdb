from django.contrib import admin
from .models import FbFederation, FbSeason,FbCompetition, FbCountry, FbLeague, FbTeam, FbStandings, FbMatch

# Register your models here.
admin.site.register(FbFederation)
admin.site.register(FbCompetition)
admin.site.register(FbCountry)
admin.site.register(FbLeague)
admin.site.register(FbTeam)
admin.site.register(FbStandings)
admin.site.register(FbSeason)
admin.site.register(FbMatch)