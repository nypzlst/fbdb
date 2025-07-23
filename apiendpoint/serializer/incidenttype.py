from rest_framework import serializers
from db.models import TypeIncident

class IncidentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeIncident
        fields = '__all__'
        