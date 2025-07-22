from rest_framework import serializers
from db.models import CountryList

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryList
        fields = '__all__'
        

