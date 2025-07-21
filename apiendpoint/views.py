from django.shortcuts import render
from .serializers import CountrySerializer
from rest_framework import viewsets
from db.models import CountryList
# Create your views here.

class CountryViewSet(viewsets.ModelViewSet):
    queryset = CountryList.objects.all().order_by()
    serializer_class = CountrySerializer
    
