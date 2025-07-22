from django.shortcuts import render
from .serializer.country import CountrySerializer
from rest_framework import viewsets
from db.models import CountryList
from rest_framework.permissions import IsAuthenticatedOrReadOnly, BasePermission
from rest_framework.decorators import action
from rest_framework.response import Response
# Create your views here.

class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return request.user and request.user.is_staff



class CountryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStaffOrReadOnly]
    queryset = CountryList.objects.all().order_by('country_name')
    serializer_class = CountrySerializer
    
    
    
    
   
