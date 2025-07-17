# type of views.py

from django.http import JsonResponse
from django.shortcuts import render
from .models import ColorectalCancerData, LungCancerData, BreastCancerData, ProstateCancerData, GastricCancerData  # Import other models as needed
from django.core.serializers import serialize
import json
from .discription import *

def get_cancer_data(request, cancer_type):
    # Map cancer type to model
    model_map = {
        'colorectal': ColorectalCancerData,
        'lung': LungCancerData,
        'breast': BreastCancerData,
        'prostate': ProstateCancerData,
        'gastric': GastricCancerData,
        # Add other cancer types here
    }

    if cancer_type not in model_map:
        return JsonResponse({'error': 'Invalid cancer type'}, status=400)

    model = model_map[cancer_type]

    # Get column names (excluding internal fields like id)
    columns = [field.name for field in model._meta.fields if field.name != 'id']
    
    # Get data
    data = list(model.objects.values(*columns))
    
    # Prepare response
    response = {
        'columns': columns,
        'data': data
    }
    for row in data:
        # Handle text column (CANCER SCREENING)
        if 'CANCER SCREENING' in row and (row['CANCER SCREENING'] is None or row['CANCER SCREENING'] == ''):
            row['CANCER SCREENING'] = 'No description available'


    return JsonResponse(response)

