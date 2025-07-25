from .BaseView import BaseAdminViewSet
from db.models import CountryList
from ..serializer.country import CountrySerializer

class CountryViewSet(BaseAdminViewSet):
    queryset = CountryList.objects.all()
    serializer_class = CountrySerializer
    filterset_fields =['country_name','iso_code']

    
    
    
    
   
