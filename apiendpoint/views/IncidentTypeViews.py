from rest_framework.viewsets import ModelViewSet
from db.models import TypeIncident
from ..permissons import IsStaffOrReadOnly

class IncidentTypeViewSet(ModelViewSet):
    permission_classes = [IsStaffOrReadOnly]
    queryset = TypeIncident.objects.all()