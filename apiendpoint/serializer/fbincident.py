from rest_framework.serializers import ModelSerializer 
from db.models import FbIncident

class FbIncidentSerializer(ModelSerializer):
    class Meta:
        model = FbIncident
        fields = '__all__'
        