from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser

class BaseAdminViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    lookup_field = 'slug'
