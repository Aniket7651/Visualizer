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
from .api import get_cancer_data
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', Infra, name='infra'),
    path('get_map_data/', get_map_data, name='get_map_data'),
    path('get_histogram_data/', get_histogram_data, name='get_histogram_data'),

    path('index/', index, name='index'),
    path('data/', datasetView, name='datasetView'),

    path('api/cancer/<str:cancer_type>/', get_cancer_data, name='get_cancer_data'), # API link for cancer data
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
