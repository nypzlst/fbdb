from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser
from db.models import TypeIncident
from ..serializer.incidenttype import IncidentTypeSerializer

class IncidentTypeViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = TypeIncident.objects.all()
    serializer_class = IncidentTypeSerializer
    filter_backends = [DjangoFilterBackend]
    lookup_field = 'slug'