from rest_framework import serializers
from db.models import IncidentClass

class IncidentClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentClass
        fields = '__all__'