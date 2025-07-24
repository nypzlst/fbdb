from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser
from db.models import CountryList
from ..serializer.country import CountrySerializer



class CountryViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = CountryList.objects.all()
    serializer_class = CountrySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields =['country_name','iso_code']
    lookup_field = 'slug'
    
    
    
    
   
