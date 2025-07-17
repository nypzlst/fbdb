from django.db import models
from .additionlist import Type_of_conf
from partial_date import PartialDateField


class FootballFederationM(models.Model):
    class Meta:
        verbose_name = 'FootballFederation'
        verbose_name_plural = 'FootballFederations'
    
    Fed_Name = models.CharField(max_length=20)
    Type_Fed = models.CharField(
        max_length=2,
        choices=Type_of_conf
    )
    Founded_Year = PartialDateField()
    Members = models.IntegerField(help_text="Dont counting associate members")
    Associate_Member = models.IntegerField(
        help_text="Members who not full join to federation. Default value 0",
        blank=True,
        default=0
    )
    Main_tournament = models.CharField()
    def __str__(self):
        return self.Fed_Name
# TODO: ограничение для Member, Associate_Member - только положительные числа


class FootballAssociate(models.Model):
    pass


