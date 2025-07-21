from rest_framework import serializers
from db.models import CountryList

class CountrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CountryList
        fields = ['country_name','iso_code']