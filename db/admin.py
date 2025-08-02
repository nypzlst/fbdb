from django.contrib import admin
from .models import Country, Season,Competition, Stadium,OrganizationMember, Organization, Match,Team


admin.site.register(Country)
admin.site.register(Competition)
admin.site.register(OrganizationMember)
admin.site.register(Team)
admin.site.register(Match)
admin.site.register(Stadium)
admin.site.register(Season)
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
    
    
