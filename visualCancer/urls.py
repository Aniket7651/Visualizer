"""
URL configuration for visualCancer project.

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
from django.urls import path
from .views import *
from .api import get_cancer_data, stats_data, get_CountryStatJSON
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    # path('', Infra, name='infra'), # root path
    path('get_map_data/', get_map_data, name='get_map_data'),
    path('get_histogram_data/', get_histogram_data, name='get_histogram_data'),

    path('', index, name='index'), # path 'index/' root path current time
    path('data/', datasetView, name='datasetView'),
    path('api/', apiAccess, name='apiAccess'),

    path('api/cancer/<str:cancer_type>/', get_cancer_data, name='get_cancer_data'), # API link for cancer data
    path('api/stats/<str:cancer_type>/', stats_data, name='stats_data'),  # API link for statistics data
    path('api/stats/country_Wise/<str:cancer_type>/', get_CountryStatJSON, name='country_stat'), 
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
