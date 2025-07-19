from django.contrib import admin
from .models import FbFederation, FbSeason,FbSubstitution,FbCompetition, FbCountry, FbLeague, FbTeam, FbStandings, FbGoal,FbMatch,FbPlayer,FbIncident
from .models import CountryList, TypeIncedent, IncidentClass
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
admin.site.register(FbIncident)
admin.site.register(FbGoal)
admin.site.register(FbSubstitution)
admin.site.register(CountryList)
admin.site.register(TypeIncedent)
admin.site.register(IncidentClass)
