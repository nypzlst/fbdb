from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser
from db.models import IncidentClass
from ..serializer.incidentclass import IncidentClassSerializer

class  IncidentClassViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = IncidentClass.objects.all()
    serializer_class = IncidentClassSerializer
    filter_backends = [DjangoFilterBackend]
    lookup_field = 'slug'

 