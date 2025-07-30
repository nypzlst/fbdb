from django.contrib import admin
# from .models import FbFederation, FbSeason,FbSubstitution,FbCompetition, FbCountry, FbLeague, FbTeam, FbStandings, FbGoal,FbMatch,FbPlayer
# from .models import CountryList, TypeIncident, IncidentClass, FbIncident
# Register your models here.
from .models import Country, Competition, OrganizationMember, Organization


admin.site.register(Country)
admin.site.register(Competition)
admin.site.register(OrganizationMember)

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'acronym_name', 'members_count','associate_member_count','total_member',)  # <-- тут свойство
    readonly_fields = ('members_count','associate_member_count','total_member',)  # если хотите видеть на детальной странице

    # Если хотите, чтобы свойство отображалось с красивым заголовком:
    def members_count(self, obj):
        return obj.members_count_without_associate
    members_count.short_description = 'Количество участников'
    
    def associate_member_count(self,obj):
        return obj.associate_member_count
    associate_member_count.short_description = 'Количество асоциативных учасников'
    
    def total_member(self, obj):
        return obj.total_member
    total_member.short_description = 'Количество всех участников'
    
    
# admin.site.register(FbIncident)
# admin.site.register(FbFederation)
# admin.site.register(FbCompetition)
# admin.site.register(FbCountry)
# admin.site.register(FbLeague)
# admin.site.register(FbTeam)
# admin.site.register(FbStandings)
# admin.site.register(FbSeason)
# admin.site.register(FbMatch)
# admin.site.register(FbPlayer)
# admin.site.register(FbGoal)
# admin.site.register(FbSubstitution)
# admin.site.register(TypeIncident)
# admin.site.register(IncidentClass)
