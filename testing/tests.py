from django.test import TestCase
from db.models import CountryList, FbCompetition, TypeCompetition,TypeIncedent,IncidentClass, TypeConference, FbFederation,TypeCompetition

# Create your tests here.

class DbTestCase(TestCase):
    def setUp(self):

        CountryList.objects.create(country_name='England',iso_code = 'EN')
        CountryList.objects.create(country_name='France',iso_code = 'FR')

        TypeIncedent.objects.create(name_incident='goal')
        TypeIncedent.objects.create(name_incident='card')

        IncidentClass.objects.create(class_incident='goal')
        IncidentClass.objects.create(class_incident='yellow')

        self.competition1 = FbCompetition.objects.create(competition_name='FIFA World Cup',
                                     type_competition=TypeCompetition.TOURNAMENT)
        self.competition2 = FbCompetition.objects.create(competition_name='FIFA Club World Cup',
                                     type_competition=TypeCompetition.TOURNAMENT)


        

    def test_federation(self):

        federation = FbFederation.objects.create(
            name_fed = 'Fédération internationale de football association',
            acronym_fed = 'FIFA',
            type_fed = TypeConference.CONTINENTAL,
            founded_year = 1954,
            members_count = 221,
            associate_member_count = 0,
            main_tournament = self.competition1
        )
        federation.other_tournament.add(self.competition2)
        self.assertEqual(federation.acronym_fed, 'FIFA')

