from db.models import FbIncident
from ..serializer.fbincident import FbIncidentSerializer
from .BaseView import BaseAdminViewSet

class FbincidentViewSet(BaseAdminViewSet):
    queryset = FbIncident.objects.all()
    serializer_class = FbIncidentSerializer
    filterset_fields =['match_where_incident','incident_type','incident_class']
    