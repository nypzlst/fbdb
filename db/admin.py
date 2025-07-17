from django.contrib import admin
from .models import CountryFootball, FootballFederationM,FootballLeague,FootballCompetition

# Register your models here.
admin.site.register(FootballFederationM)
admin.site.register(CountryFootball)
admin.site.register(FootballLeague)
admin.site.register(FootballCompetition)
