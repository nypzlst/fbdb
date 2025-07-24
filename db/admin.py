from django.contrib import admin
from .models import FbFederation, FbSeason,FbSubstitution,FbCompetition, FbCountry, FbLeague, FbTeam, FbStandings, FbGoal,FbMatch,FbPlayer
from .models import CountryList, TypeIncident, IncidentClass
# Register your models here.

@admin.register(CountryList)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('country_name','iso_code','slug')
    prepopulated_fields = {"slug":("country_name",)}


admin.site.register(FbFederation)
admin.site.register(FbCompetition)
admin.site.register(FbCountry)
admin.site.register(FbLeague)
admin.site.register(FbTeam)
admin.site.register(FbStandings)
admin.site.register(FbSeason)
admin.site.register(FbMatch)
admin.site.register(FbPlayer)
admin.site.register(FbGoal)
admin.site.register(FbSubstitution)
admin.site.register(TypeIncident)
admin.site.register(IncidentClass)
