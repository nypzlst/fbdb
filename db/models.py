from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from django.db.models import Q
from django.utils.text import slugify
from .slugtitlesave import SlugTitleSaver

#region Choices Models
""" Список для выбора типа enum"""
class PreferedFoot(models.TextChoices):
    LEFT = 'L', 'LEFT'
    RIGHT = 'R', 'RIGHT'
    BOTH = 'B', 'BOTH'

class Position(models.TextChoices):
    GOALKEEPER = 'GK', 'GOALKEEPER'
    DEFENDER = 'D', 'DEFENDER'
    MIDFIELDER = 'M', 'MIDFIELDER'
    FORWARD = 'F', 'FORWARD'

class TypeConference(models.TextChoices):
    GLOBAL = 'GL','GLOBAL'
    CONTINENTAL = 'CN', 'CONTINENTAL'

#endregion


# NEW MODELS
class Organization(SlugTitleSaver, models.Model):
    class Meta:
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'
        ordering = ['acronym_name']
        
    name = models.CharField(max_length=250)
    acronym_name = models.CharField(max_length=10)    
    founded_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1850), MaxValueValidator(2100)]
    )
    type_organization = models.CharField(max_length=2,choices=TypeConference)
    slug_source_field = 'acronym_name'
    slug = models.SlugField(
        unique=True,
        blank=True
    )
    
    @property
    def members_count_without_associate(self):
        return self.member_global.filter(is_associate_member=False).count() + self.member_local.filter(is_associate_member=False).count()
    @property
    def associate_member_count(self):
        return self.member_global.filter(is_associate_member=True).count() + self.member_local.filter(is_associate_member=True).count()
    @property
    def total_member(self):
        return self.member_global.count()+ self.member_local.count()
    
    
    def __str__(self):
        return self.acronym_name
    
    def clean(self):
        super().clean()
        if not self.pk:
            return

        if not hasattr(self, 'member_countries'):
            return
        
        if self.associate_member_count > self.members_count:
            raise ValidationError({
            'associate_member_count': "Должно быть не больше, чем members_count."
        })




class OrganizationMember(SlugTitleSaver,models.Model):
    class Meta:
        verbose_name = 'Organization Member'
        verbose_name_plural = 'Organization Members'
        ordering = ['name']
        
    name = models.CharField(max_length=200)
    country = models.OneToOneField('Country', on_delete= models.CASCADE)
    slug = models.SlugField(unique=True,blank=True)
    is_associate_member = models.BooleanField(default=False)
    
    global_organizer = models.ForeignKey(
        'Organization',
        on_delete=models.CASCADE,
        related_name='member_global',
        limit_choices_to={'acronym_name': 'FIFA'}, 
        null=True,
        blank=True,
        verbose_name="Global Organizer"
    )
    local_organizer = models.ForeignKey(
        'Organization',
        on_delete=models.CASCADE,
        related_name='member_local',
        limit_choices_to=~models.Q(acronym_name='FIFA'),
        null=True,
        blank=True,
        verbose_name="Regional Organizer"
    )
    
    def __str__(self):
        return self.name



class Competition(SlugTitleSaver, models.Model):
    class Meta:
        verbose_name = 'Competition'
        verbose_name_plural = 'Competitions'
        ordering = ['name']
        
    class TypeCompetition(models.TextChoices):
        CLUB = 'CLUB', 'club competition'
        NATIONAL = 'NAT', 'national team competition'
    
    class TierCompetition(models.TextChoices):
        FIRSTCUP = '1tierC', '1-st-tier cup'
        SECONDCUP = '2tierC', '2nd-tier cup'
        THIRDCUP = '3tierC', '3rd-tier cup'
        FIRSTLEAGUE = '1tierL', '1-st-tier league'
        SECONDLEAGUE = '2tierL', '2nd-tier league'
        THIRDLEAGUE = '3tierL', '3rd-tier league'
        FOURTHLEAGUE = '4tierL', '4th-tier league'
        FIFTHLEAGUE = '5tierL', '5th-tier league'
        SIXTHLEAGUE = '6tierL', '6th-tier league'
        SEVENTHLEAGUE = '7tierL', '7th-tier league'
        EIGHTLEAGUE = '8tierL', '8th-tier league'
        NINTHLEAGUE = '9tierL', '9th-tier league'
        TENTHLEAUGUE = '10tierL', '10th-tier league'
        ELEVENTHLEAUGUE = '11tierL', '11th-tier league'
        NATIONALCUP = 'nacup', 'national cup'
        LEAGUECUP = 'lcup', 'league cup'
        SUPERCUP = 'supcup', 'super cup'
        LOWERCUP = 'lowcup', 'lower cup'
    
    
    name = models.CharField(max_length=200, unique=True)
    type = models.CharField(max_length=4, choices=TypeCompetition)
    tier = models.CharField(max_length=10, choices=TierCompetition,blank=True)
    organizer = models.ForeignKey('Organization', on_delete=models.SET_NULL,null=True,blank=True)
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, blank=True, null=True)
    slug = models.SlugField(unique=True,blank=True)

    def clean(self):
        super().clean()
        if self.type == self.TypeCompetition.NATIONAL and self.tier:
            raise ValidationError ({
                'tier' : _('national competition cannot have a tier')
            })

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"



class Country(models.Model):
    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        ordering = ['name']
    
    name = models.CharField(max_length=200)
    iso_code = models.CharField(max_length=2)

    def __str__(self):
        return self.name


class Match(SlugTitleSaver, models.Model):
    class Meta:
        verbose_name = 'Match'
        verbose_name_plural = 'Matches'
        
    home_team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='home_matches')
    away_team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='away_matches')
    home_score = models.IntegerField()
    away_score = models.IntegerField()

    stadium = models.ForeignKey('Stadium', on_delete=models.CASCADE)
    tournament = models.ForeignKey('Competition', on_delete=models.CASCADE)
    season = models.ForeignKey('Season',on_delete=models.CASCADE)
    
    match_day = models.DateField()
    slug_source_field = ['home_team','away_team','season','match_day']
    
    slug = models.SlugField(unique=True,blank=True)
    
    def clean(self):
        super().clean()

        if self.home_team == self.away_team:
            raise ValidationError({
                'away_team':'Однинаковые команды выбраны'
            })
        conflict_match = Match.objects.filter(
                match_day=self.match_day
            ).filter(
                Q(home_team=self.home_team) | Q(home_team=self.away_team) |
                Q(away_team=self.home_team) | Q(away_team=self.away_team)
            )
        if self.pk:
            conflict_match = conflict_match.exclude(pk=self.pk)

        if conflict_match.exists():
            raise ValidationError('В этот день уже существует матч')
    
    def __str__(self):
        return f'{self.home_team} - {self.away_team} = {self.season} - {self.match_day}'

class Team(models.Model):
    name = models.CharField(max_length=200)

class Stadium(models.Model):
    name = models.CharField(max_length=200)

class Season(models.Model):
    class Meta:
        verbose_name = 'Season'
        verbose_name_plural = 'Seasons'
        ordering = ['competition']
        
    competition = models.ForeignKey('Competition', on_delete=models.CASCADE)
    season_start = models.DateField()
    season_end = models.DateField()
    slug_source_field = ['competition','season_start','season_end']
    slug = models.SlugField(unique=True,blank=True)
    
    def __str__(self):
        return f"{self.competition} = {self.season_start} - {self.season_end}"
    
# CREATED MODELS : Season, Match, Organization, OrganizationMember, Country, Competition 
# NEEDED MODELS : Incident, Goal, SwapPlayer, Player, Standings, League, Type and class Incident
    
# OLD MODELS




# """ Сущность футбольной лиги """
# class FbLeague(SlugTitleSaver,models.Model):
#     class Meta:
#         verbose_name = 'Football League'
#         verbose_name_plural = 'Football Leagues'
#         ordering = ['name']
    
#     name = models.ForeignKey(
#         'FbCompetition',
#         on_delete=models.CASCADE,
#         limit_choices_to={'type_competition' : 'L'}
#     )
#     slug = models.SlugField(unique=True, blank=True)
#     country_league = models.ForeignKey(
#         'FbcountryFed',
#         on_delete=models.CASCADE
#     ) # желательно хранить страну, хотя лучше подумать над этим
#     count_team_in_league = models.IntegerField(default=0)
#     # TODO вычеслять по фактическому количеству команд
#     def __str__(self):
#         return str(self.name)



# """ Футбольные команды """
# class FbTeam(SlugTitleSaver, models.Model):
#     class Meta:
#         verbose_name = 'Футбольная команда'
#         verbose_name_plural = 'Футбольные команды'
#         ordering = ['name']
    
#     name = models.CharField(max_length=50)
#     slug = models.SlugField(unique=True, blank=True)
#     league_where_play_team = models.ManyToManyField(FbLeague)
#     def __str__(self):
#         return self.name

# class FbPlayer(SlugTitleSaver, models.Model):
#     class Meta:
#         verbose_name = 'Игрок'
#         verbose_name_plural = 'Игроки'
#         ordering = ['short_name']
    
#     full_name = models.CharField(max_length=100)
#     short_name = models.CharField(max_length=50)
    
#     position = models.CharField(max_length=2,choices=Position.choices)
#     prefered_foot = models.CharField(max_length=2,choices=PreferedFoot.choices)
    
#     jersey_number = models.PositiveIntegerField(
#         validators=[MinValueValidator(0), MaxValueValidator(100)]
#     )
#     height = models.PositiveIntegerField()
#     date_of_birthday = models.DateField()
#     slug_source_field ='short_name'
#     slug = models.SlugField(unique=True, blank=True)
#     national = models.ForeignKey('CountryList',on_delete=models.CASCADE)
#     played_in_team = models.ForeignKey(FbTeam, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.full_name



# """ Сущность турнирной таблицы """
# class FbStandings(SlugTitleSaver,models.Model):
#     class Meta:
#         verbose_name = 'Позиция команды в турнире'
#         verbose_name_plural = 'Позиция команды в турнирах'
#         unique_together = ('season_year', 'team', 'standing_league')

#     season_year = models.ForeignKey('FbSeason', on_delete=models.CASCADE)
#     standing_league = models.ForeignKey('FbLeague', on_delete=models.CASCADE)
#     team = models.ForeignKey('FbTeam', on_delete=models.CASCADE)

#     match_played_count = models.PositiveIntegerField(default=0)
#     win_match_count = models.PositiveIntegerField(default=0)
#     lost_match_count = models.PositiveIntegerField(default=0)
#     draw_match_count = models.PositiveIntegerField(default=0)
    
#     difference_goal = models.IntegerField(default=0)
#     scored_goal = models.PositiveIntegerField(default=0)
#     missed_goal = models.PositiveIntegerField(default=0)

#     last_five_match = ArrayField(
#         base_field=models.CharField(max_length=1),
#         size=5,
#         default=list,
#         blank=True,
#         null=True
#     )
#     slug_source_field = ['season_year','team']
#     slug = models.SlugField(unique=True, blank=True)
    
    
#     def __str__(self):
#         return f"{self.team} - {self.season_year}"
#     def clean(self):
#         if self.win_match_count + self.lost_match_count + self.draw_match_count != self.match_played_count:
#             raise ValidationError("Сумма побед, поражений и ничьих не равна общему количеству матчей")
    
# # TODO: кеширование через редис
# # TODO: заполнить таблицу как на софаскор



# """ Начала сезонов для лиги"""
# class FbSeason(SlugTitleSaver, models.Model):
#     class Meta:
#         verbose_name = 'Сезон'
#         verbose_name_plural = 'Сезоны'
#         ordering = ['name_league']
#     # какой-то кал выходит по названию, так то это название лиги и её старт и конец
#     name_league = models.ForeignKey( 
#         'FbLeague',
#         on_delete=models.CASCADE, 
#         related_name='seasons',
#     )
#     start_season_year = models.PositiveIntegerField(
#         validators=[MinValueValidator(1850), MaxValueValidator(2100)]
#     )
#     end_season_year = models.PositiveIntegerField(
#         validators=[MinValueValidator(1850), MaxValueValidator(2100)]
#     )
#     slug_source_field = ['name_league','start_season_year','end_season_year']
#     slug = models.SlugField(unique=True, blank=True)
    
#     def __str__(self):
#         return f"{self.name_league} - {str(self.start_season_year)[-2:]}/{str(self.end_season_year)[-2:]}"
#     def clean(self):
#         super().clean()

#         if self.start_season_year == self.end_season_year:
#             raise ValidationError({
#                 'start_season_year' : 'Год старта такой же как и год конца'
#             })
#         if self.start_season_year > self.end_season_year:
#             raise ValidationError({
#                 'start_season_year' : 'Год старта больше чем год конца'
#             })
#         if (self.end_season_year-self.start_season_year) > 1:
#             raise ValidationError({
#                 'end_season_year' : 'Год старта больше чем год конца'
#             })
#     # TODO: не забыть сериализацию для АПИ !!!
#     # TODO: сделать таблицу матчей - Делаеться 



# # region Match Table
# """ Создание статистики матчей на основе АПИ sofascore"""
# class FbMatch(SlugTitleSaver, models.Model):
#     class Meta():
#         verbose_name = 'Матч'
#         verbose_name_plural = 'Матчи'
    
    
#     match_on_league = models.ForeignKey(
#         FbLeague,
#         on_delete=models.CASCADE,
#         related_name='league_match'
#     )
#     season = models.ForeignKey('FbSeason', on_delete=models.CASCADE)
#     home_team = models.ForeignKey(
#         FbTeam,
#         on_delete=models.CASCADE,
#         related_name='home_team'
#     )
#     away_team = models.ForeignKey(
#         FbTeam,
#         on_delete=models.CASCADE,
#         related_name='away_team'
#     )
#     slug_source_field = ['match_on_league','home_team','away_team']
#     slug = models.SlugField(unique=True, blank=True)

#     home_team_score = models.PositiveSmallIntegerField(default=0)
#     away_team_score = models.PositiveSmallIntegerField(default=0)

#     match_time = models.DateTimeField(db_index=True)


#     def clean(self):
#         super().clean()

#         if self.home_team == self.away_team:
#             raise ValidationError({
#                 'away_team':'Однинаковые команды выбраны'
#             })
#         conflict_match = FbMatch.objects.filter(
#             Q(home_team = self.home_team) | Q(away_team =self.away_team)|
#             Q(home_team = self.away_team) | Q(away_team = self.home_team),
#             match_time__date = self.match_time.date()
#         ) 
#         if self.pk:
#             conflict_match = conflict_match.exclude(pk=self.pk)

#         if conflict_match.exists():
#             raise ValidationError('В этот день уже существует матч')
#     # TODO можна изменить чтобы матч и тут и в апи одинаково проверялись

#     def __str__(self):
#         return f"{self.home_team} - {self.away_team} {self.match_time}"
    

# class FbIncident(SlugTitleSaver,models.Model):
#     class Meta():
#         verbose_name = 'Football Incident'
#         verbose_name_plural = 'Football Incidents'

#     match_where_incident = models.ForeignKey(
#         FbMatch,
#         on_delete=models.CASCADE
#     )
#     time_where_incedent_make = models.PositiveIntegerField()
#     is_own_goal = models.BooleanField()
#     is_home = models.BooleanField() 
#     incident_type = models.ForeignKey(
#         'TypeIncident',
#         on_delete=models.CASCADE
#     )
#     incident_class = models.ForeignKey(
#         'IncidentClass',
#         on_delete=models.CASCADE
#     )
#     description = models.CharField(max_length=150, blank=True)
#     reason = models.CharField(max_length=50, blank=True)
#     slug = models.SlugField(unique=True, blank=True)
#     slug_source_field = ['match_where_incident','incident_class']
    
#     def __str__(self):
#         return f"{str(self.match_where_incident)}"


# #skip slug
# class FbGoal(models.Model):
#     class Meta():
#         verbose_name = 'Football Goal'
#         verbose_name_plural = 'Football Goals'
    
#     incedent_goal = models.ForeignKey(
#         FbIncident,
#         on_delete=models.CASCADE
#     )
#     player_who_scored = models.ForeignKey(
#         FbPlayer,
#         on_delete=models.CASCADE,
#         related_name='player_scored'
#     )
#     player_who_assist = models.ForeignKey(
#         FbPlayer,
#         on_delete=models.CASCADE,
#         related_name='player_assist',
#         blank=True,
#         null= True
#     )
#     def __str__(self):
#         return f"{str(self.incedent_goal)}"


# #skip slug
# class FbSubstitution(models.Model):
#     class Meta():
#         verbose_name = 'Football substitution'
#         verbose_name_plural = 'Football substitutions'
    
#     incedent_substitution = models.ForeignKey(
#         FbIncident,
#         on_delete=models.CASCADE
#     )
#     player_who_in = models.ForeignKey(
#         FbPlayer,
#         on_delete=models.CASCADE,
#         related_name='player_in'
#     )
#     player_who_out = models.ForeignKey(
#         FbPlayer,
#         on_delete=models.CASCADE,
#         related_name='player_out',
#     )
#     def clean(self):
#         super().clean()
#         if self.player_who_in == self.player_who_out:
#             raise ValidationError('Не может быть что игроки совпадают')
#         # TODO сделать учет максимального количества замен или подумать над этим
#     def __str__(self):
#         return f"{str(self.incedent_substitution)}"
# # endregion


    

# class TypeIncident(SlugTitleSaver, models.Model):
#     class Meta:
#         verbose_name = "Incedent"
#         verbose_name_plural = "Incedents"
#         ordering = ['name_incident']
        
#     slug_source_field = 'name_incident'
#     name_incident = models.CharField(max_length=50, unique=True)
#     description_incident = models.CharField(max_length=200, blank=True)
#     slug = models.SlugField(unique=True, blank=True)
    
#     class_incident = models.ForeignKey(
#         'IncidentClass',
#         on_delete=models.CASCADE
#     )

#     def __str__(self):
#         return self.name_incident
    
    

# class IncidentClass(SlugTitleSaver, models.Model):
#     class Meta:
#         verbose_name = 'Football Incident Class'
#         verbose_name_plural = 'Football Incident Clases'
#         ordering = ['class_incident']
    
#     slug_source_field = 'class_incident'
#     class_incident = models.CharField(max_length=50)
#     description = models.CharField(max_length=200,blank=True)
#     slug = models.SlugField(unique=True, blank=True)
    
#     def __str__(self):
#         return self.class_incident
# #endregion







# TODO Уточнить связи моделей: Для связи FbGoal и FbSubstitution с FbIncident лучше использовать
#  OneToOneField вместо ForeignKey, так как одно событие в матче 
# (гол, замена) соответствует одной записи об инциденте.


