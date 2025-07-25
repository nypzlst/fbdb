from db.models import IncidentClass
from ..serializer.incidentclass import IncidentClassSerializer
from .BaseView import BaseAdminViewSet

class IncidentClassViewSet(BaseAdminViewSet):
    queryset = IncidentClass.objects.all()
    serializer_class = IncidentClassSerializer
    
    
 