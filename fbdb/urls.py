"""
URL configuration for fbdb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

# from apiendpoint.views import CountryViews,IncidentTypeViews, IncidentClassView, FootballIncidentView


router = routers.DefaultRouter()
# router.register(r'country', CountryViews.CountryViewSet)
# router.register(r'incidenttype', IncidentTypeViews.IncidentTypeViewSet)
# router.register(r'incidentclass', IncidentClassView.IncidentClassViewSet)
# router.register(r'fbincident', FootballIncidentView.FbincidentViewSet)
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-token-auth/',obtain_auth_token),
    path('api-test/', include('rest_framework.urls',namespace='rest_framework'))
]
