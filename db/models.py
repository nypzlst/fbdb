from django.db import models
from .additionlist import Type_of_conf, Type_of_Competition
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField

""" Федерации в духе FIFA, UEFA ..."""
class FbFederation(models.Model):
    class Meta:
        verbose_name = 'Football Federation'
        verbose_name_plural = 'Football Federations'
        ordering = ['acronym_fed']

    name_fed = models.CharField(max_length=100, unique=True)
    acronym_fed = models.CharField(max_length=10, unique=True)

    type_fed = models.CharField(
        max_length=2,
        choices=Type_of_conf
    )
    founded_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1850), MaxValueValidator(2100)]
    )

    members_count = models.PositiveIntegerField(help_text=_("Dont counting associate members"))
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
        related_name='secondary_federation'
    )

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
        verbose_name_plural = 'Football Competions'
        ordering = ['competition_name']
    
    competition_name = models.CharField(max_length=50)
    
    type_competition = models.CharField(
        max_length=1,
        choices = Type_of_Competition,
        blank=True
    )
    
    def __str__(self):
        return f"{self.competition_name} {self.get_type_competition_display()}"
    # TODO: если что убрать приписку лига или турнир здесь



""" Страна и федерация её """
class FbCountry(models.Model):
    class Meta():
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = ['country_name']
    
    country_name = models.CharField(max_length=50)
    country_association_name = models.CharField(max_length=100)
    short_association_name = models.CharField(max_length=10)
    
    tournament_in_country = models.ManyToManyField(
        'FbCompetition',
        related_name='countries'
    )

    def __str__(self):
        return self.country_name



""" Сущность футбольной лиги """
class FbLeague(models.Model):
    class Meta:
        verbose_name = 'Football League'
        verbose_name_plural = 'Football Leagues'
    
    league_name = models.ForeignKey(
        'FbCompetition',
        on_delete=models.CASCADE
    )
    country_league = models.ForeignKey(
        'FbCountry',
        on_delete=models.CASCADE
    ) # желательно хранить страну, хотя лучше подумать над этим
    count_team_in_league = models.IntegerField(default=0)
    def __str__(self):
        return str(self.league_name)



""" Футбольные команды """
class FbTeam(models.Model):
    class Meta:
        verbose_name = 'Football Team'
        verbose_name_plural = 'Football Teams'
    
    team_name = models.CharField(max_length=50)
    def __str__(self):
        return self.team_name
    


""" Сущность турнирной таблицы """
class FbStandings(models.Model):
    class Meta:
        verbose_name = 'Football Standing'
        verbose_name_plural = 'Football Standings'

    season_year = models.ForeignKey(
        'FbSeason',
        on_delete=models.CASCADE
    )
    standing_league = models.ForeignKey(
        'FbLeague',
        on_delete=models.CASCADE
    )
    team = models.ForeignKey(
        'FbTeam',
        on_delete=models.CASCADE
    )

    match_played_count = models.PositiveIntegerField()
    win_match_count = models.PositiveIntegerField()
    losse_match_count = models.PositiveIntegerField()
    draw_match_count = models.PositiveIntegerField()
    
    difference_goal = models.IntegerField()
    scored_goal = models.PositiveIntegerField()
    missed_goal = models.PositiveIntegerField()

    last_five_match = ArrayField(
        base_field=models.CharField(max_length=1),
        size=5,
        default=list
    )
# TODO: кеширование через редис
# TODO: заполнить таблицу как на софаскор



""" Начала сезонов для лиги"""
class FbSeason(models.Model):
    class Meta:
        verbose_name = 'Football Season'
        verbose_name_plural = 'Football Seasons'
        ordering = ['name_league']
    name_league = models.ForeignKey( # какой-то кал выходит по названию, так то это название лиги и её старт и конец
        'FbLeague',
        on_delete=models.CASCADE,
        related_name='season'
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
        