from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from db.models import TypeIncident
from ..permissons import IsStaffOrReadOnly
from ..serializer.incidenttype import IncidentTypeSerializer

class IncidentTypeViewSet(ModelViewSet):
    permission_classes = [IsStaffOrReadOnly]
    queryset = TypeIncident.objects.all()
    serializer_class = IncidentTypeSerializer
    filter_backends = [DjangoFilterBackend]
    lookup_field = 'slug'