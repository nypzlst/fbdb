from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from db.models import CountryList

from ..permissons import IsStaffOrReadOnly
from ..serializer.country import CountrySerializer



class CountryViewSet(ModelViewSet):
    permission_classes = [IsStaffOrReadOnly]
    queryset = CountryList.objects.all()
    serializer_class = CountrySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields =['country_name','iso_code']
    lookup_field = 'slug'
    
    
    
    
   
