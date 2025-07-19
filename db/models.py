from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from django.db.models import Q

#region Choices Models
""" Список для выбора типа enum"""
class PreferedFoot(models.TextChoices):
    LEFT = 'L', 'LEFT',
    RIGHT = 'R', 'RIGHT',
    BOTH = 'B', 'BOTH'

class Position(models.TextChoices):
    GOALKEEPER = 'GK', 'GOALKEEPER',
    DEFENDER = 'D', 'DEFENDER',
    MIDFIELDER = 'M', 'MIDFIELDER',
    FORWARD = 'F', 'FORWARD'

class TypeConference(models.TextChoices):
    GLOBAL = 'GL','GLOBAL',
    CONTINENTAL = 'CN', 'CONTINENTAL'

class TypeCompetition(models.TextChoices):
    TOURNAMENT = 'T', 'TOURNAMENT',
    LEAGUE = 'L', 'LEAGUE'
#endregion



""" Федерации в духе FIFA, UEFA ..."""
class FbFederation(models.Model):
    class Meta:
        verbose_name = 'Football Federation'
        verbose_name_plural = 'Football Federations'
        ordering = ['acronym_fed']

    name_fed = models.CharField(max_length=100, unique=True)
    acronym_fed = models.CharField(max_length=10, unique=True)

    type_fed = models.CharField(max_length=2, choices=TypeConference)
    founded_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1850), MaxValueValidator(2100)]
    )

    members_count = models.PositiveIntegerField(
        help_text=_("Dont counting associate members")
        )
    associate_member_count = models.PositiveIntegerField(
        help_text=_("Members who not full join to federation. Default value 0"),
        blank=True,
        default=0
    )

    main_tournament = models.OneToOneField(
        'FbCompetition',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='governing_federation'
    )
    other_tournament = models.ManyToManyField(
        'FbCompetition',
        related_name='secondary_federation')

    def __str__(self):
        return self.acronym_fed
    
    def clean(self):
        super().clean()
        if self.associate_member_count > self.members_count:
            raise ValidationError({
            'associate_member_count': "Должно быть не больше, чем members_count."
        })
    # TODO: в АПИ прокинуть защиту от того что можно основной турнир добавить в остальные



""" Список турниров """
class FbCompetition(models.Model):
    class Meta:
        verbose_name = 'Football Competition'
        verbose_name_plural = 'Football Competitions'
        ordering = ['competition_name']
    
    competition_name = models.CharField(max_length=50)
    
    type_competition = models.CharField(
        max_length=1,
        choices = TypeCompetition,
        blank=True
    )
    
    def __str__(self):
        return f"{self.competition_name} {self.get_type_competition_display()}"
    # TODO: если что убрать приписку лига или турнир здесь



""" Страна и федерация её """
class FbCountry(models.Model):
    class Meta():
        verbose_name = "Football Country"
        verbose_name_plural = "Football Countries"
        ordering = ['country_name']
    
    country_name = models.ForeignKey(
        'CountryList',
        on_delete=models.CASCADE)
    country_association_name = models.CharField(max_length=100)
    short_association_name = models.CharField(max_length=10)
    
    tournament_in_country = models.ManyToManyField(
        'FbCompetition',
        related_name='countries'
    )

    def __str__(self):
        return f"{self.country_name} - {self.country_association_name}"

# TODO приоритеты лиг сделать

""" Сущность футбольной лиги """
class FbLeague(models.Model):
    class Meta:
        verbose_name = 'Football League'
        verbose_name_plural = 'Football Leagues'
    
    league_name = models.ForeignKey(
        'FbCompetition',
        on_delete=models.CASCADE,
        limit_choices_to={'type_competition' : 'L'}
    )
    country_league = models.ForeignKey(
        'CountryList',
        on_delete=models.CASCADE
    ) # желательно хранить страну, хотя лучше подумать над этим
    count_team_in_league = models.IntegerField(default=0)
    # TODO вычеслять по фактическому количеству команд
    def __str__(self):
        return str(self.league_name)



""" Футбольные команды """
class FbTeam(models.Model):
    class Meta:
        verbose_name = 'Football Team'
        verbose_name_plural = 'Football Teams'
    
    team_name = models.CharField(max_length=50)
    league_where_play_team = models.ManyToManyField(FbCompetition)
    def __str__(self):
        return self.team_name

class FbPlayer(models.Model):
    class Meta:
        verbose_name = 'Football Player'
        verbose_name_plural = 'Football Players'
    
    full_name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=50)
    
    position = models.CharField(max_length=2,choices=Position.choices)
    prefered_foot = models.CharField(max_length=2,choices=PreferedFoot.choices)
    
    jersey_number = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    height = models.PositiveIntegerField()
    date_of_birthday = models.DateField()

    national = models.ForeignKey('CountryList',on_delete=models.CASCADE)
    played_in_team = models.ForeignKey(FbTeam, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name



""" Сущность турнирной таблицы """
class FbStandings(models.Model):
    class Meta:
        verbose_name = 'Football Standing'
        verbose_name_plural = 'Football Standings'
        unique_together = ('season_year', 'team', 'standing_league')

    season_year = models.ForeignKey('FbSeason', on_delete=models.CASCADE)
    standing_league = models.ForeignKey('FbLeague', on_delete=models.CASCADE)
    team = models.ForeignKey('FbTeam', on_delete=models.CASCADE)

    match_played_count = models.PositiveIntegerField(default=0)
    win_match_count = models.PositiveIntegerField(default=0)
    lost_match_count = models.PositiveIntegerField(default=0)
    draw_match_count = models.PositiveIntegerField(default=0)
    
    difference_goal = models.IntegerField(default=0)
    scored_goal = models.PositiveIntegerField(default=0)
    missed_goal = models.PositiveIntegerField(default=0)

    last_five_match = ArrayField(
        base_field=models.CharField(max_length=1),
        size=5,
        default=list,
        blank=True,
        null=True
    )
    def __str__(self):
        return f"{self.team} - {self.season_year}"

# TODO: кеширование через редис
# TODO: заполнить таблицу как на софаскор



""" Начала сезонов для лиги"""
class FbSeason(models.Model):
    class Meta:
        verbose_name = 'Football Season'
        verbose_name_plural = 'Football Seasons'
        ordering = ['name_league']
    # какой-то кал выходит по названию, так то это название лиги и её старт и конец
    name_league = models.ForeignKey( 
        'FbLeague',
        on_delete=models.CASCADE, 
        related_name='seasons',
    )
    start_season_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1850), MaxValueValidator(2100)]
    )
    end_season_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1850), MaxValueValidator(2100)]
    )

    def __str__(self):
        return f"{self.name_league} - {str(self.start_season_year)[-2:]}/{str(self.end_season_year)[-2:]}"
    def clean(self):
        super().clean()

        if self.start_season_year == self.end_season_year:
            raise ValidationError({
                'start_season_year' : 'Год старта такой же как и год конца'
            })
        if self.start_season_year > self.end_season_year:
            raise ValidationError({
                'start_season_year' : 'Год старта больше чем год конца'
            })
        if (self.end_season_year-self.start_season_year) > 1:
            raise ValidationError({
                'end_season_year' : 'Год старта больше чем год конца'
            })
    # TODO: не забыть сериализацию для АПИ !!!
    # TODO: сделать таблицу матчей - Делаеться 



# region Match Table
""" Создание статистики матчей на основе АПИ sofascore"""
class FbMatch(models.Model):
    class Meta():
        verbose_name = 'Football Match'
        verbose_name_plural = 'Football Matches'
    
    
    match_on_league = models.ForeignKey(
        FbLeague,
        on_delete=models.CASCADE,
        related_name='league_match'
    )

    home_team = models.ForeignKey(
        FbTeam,
        on_delete=models.CASCADE,
        related_name='home_team'
    )
    away_team = models.ForeignKey(
        FbTeam,
        on_delete=models.CASCADE,
        related_name='away_team'
    )

    home_team_score = models.PositiveSmallIntegerField(default=0)
    away_team_score = models.PositiveSmallIntegerField(default=0)

    match_time = models.DateTimeField(db_index=True)


    def clean(self):
        super().clean()

        if self.home_team == self.away_team:
            raise ValidationError({
                'away_team':'Однинаковые команды выбраны'
            })
        conflict_match = FbMatch.objects.filter(
            Q(home_team = self.home_team) | Q(away_team =self.away_team)|
            Q(home_team = self.away_team) | Q(away_team = self.home_team),
            match_time__date = self.match_time.date()
        ) 
        if self.pk:
            conflict_match = conflict_match.exclude(pk=self.pk)

        if conflict_match.exists():
            raise ValidationError('В этот день уже существует матч')
    # TODO можна изменить чтобы матч и тут и в апи одинаково проверялись

    def __str__(self):
        return f"{self.home_team} - {self.away_team} {self.match_time}"
    

class FbIncident(models.Model):
    class Meta():
        verbose_name = 'Football Incident'
        verbose_name_plural = 'Football Incidents'

    match_where_incedent = models.ForeignKey(
        FbMatch,
        on_delete=models.CASCADE
    )
    time_where_incedent_make = models.PositiveIntegerField()
    is_own_goal = models.BooleanField()
    is_home = models.BooleanField() # инцедент хозяев или нет 
    incident_type = models.ForeignKey(
        'TypeIncedent',
        on_delete=models.CASCADE
    )
    incident_class = models.ForeignKey(
        'IncidentClass',
        on_delete=models.CASCADE
    )
    description = models.CharField(max_length=150, blank=True)
    reason = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return f"{str(self.match_where_incedent)}"



class FbGoal(models.Model):
    class Meta():
        verbose_name = 'Football Goal'
        verbose_name_plural = 'Football Goals'
    
    incedent_goal = models.ForeignKey(
        FbIncident,
        on_delete=models.CASCADE
    )
    player_who_scored = models.ForeignKey(
        FbPlayer,
        on_delete=models.CASCADE,
        related_name='player_scored'
    )
    player_who_assist = models.ForeignKey(
        FbPlayer,
        on_delete=models.CASCADE,
        related_name='player_assist',
        blank=True,
        null= True
    )
    def __str__(self):
        return f"{str(self.incedent_goal)}"



class FbSubstitution(models.Model):
    class Meta():
        verbose_name = 'Football substitution'
        verbose_name_plural = 'Football substitutions'
    
    incedent_substitution = models.ForeignKey(
        FbIncident,
        on_delete=models.CASCADE
    )
    player_who_in = models.ForeignKey(
        FbPlayer,
        on_delete=models.CASCADE,
        related_name='player_in'
    )
    player_who_out = models.ForeignKey(
        FbPlayer,
        on_delete=models.CASCADE,
        related_name='player_out',
    )
    def clean(self):
        super().clean()
        if self.player_who_in == self.player_who_out:
            raise ValidationError('Не может быть что игроки совпадают')
        # TODO сделать учет максимального количества замен или подумать над этим
    def __str__(self):
        return f"{str(self.incedent_substitution)}"
# endregion


# region Addition Models
""" Вспомогательные таблицы """
class CountryList(models.Model):
    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = ['country_name']

    country_name = models.CharField(max_length=150)
    iso_code = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return f'{self.country_name} - {self.iso_code}'

class TypeIncedent(models.Model):
    class Meta:
        verbose_name = "Incedent"
        verbose_name_plural = "Incedents"
        ordering = ['name_incident']

    name_incident = models.CharField(max_length=50)
    description_incident = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name_incedent
class IncidentClass(models.Model):
    class Meta:
        verbose_name = 'Football Incident Class'
        verbose_name_plural = 'Football Incident Clases'
        ordering = ['class_incident']

    class_incident = models.CharField(max_length=50)
    description = models.CharField(max_length=200,blank=True)
    def __str__(self):
        return self.class_incident
#endregion

# TODO Уточнить связи моделей: Для связи FbGoal и FbSubstitution с FbIncident лучше использовать
#  OneToOneField вместо ForeignKey, так как одно событие в матче 
# (гол, замена) соответствует одной записи об инциденте.