from db.models import TypeIncident
from ..serializer.incidenttype import IncidentTypeSerializer
from .BaseView import BaseAdminViewSet

class IncidentTypeViewSet(BaseAdminViewSet):
    queryset = TypeIncident.objects.all()
    serializer_class = IncidentTypeSerializer
 
 