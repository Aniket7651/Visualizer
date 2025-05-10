from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.conf import settings
from .models import *
from django.views.decorators.clickjacking import xframe_options_exempt

def Infra(request):
    if request.method == 'POST':
        selected_database = request.POST.get('cancerType')
        settings.CANCER_TYPES = selected_database
        print("settings.CANCER_TYPES:", settings.CANCER_TYPES)
    return render(request, 'Infra.html', {'title': 'Infrastructure'})

def UB(request):
    return render(request, 'UB.html', {'title': 'Utilization of Biomarker'})

def cancerScreen(request):
    return render(request, 'cancerScreen.html', {'title': 'Cancer Screening'})

def remb(request):
    return render(request, 'remb.html', {'title': 'Reimbursement'})

def care(request):
    return render(request, 'care.html', {'title': 'Survival Rates, Early Detection and Palliative Care'})