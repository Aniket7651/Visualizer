from django.http import JsonResponse
from django.shortcuts import render
from .models import ColorectalCancerData, LungCancerData, BreastCancerData, ProstateCancerData, GastricCancerData  # Import other models as needed
from django.core.serializers import serialize
import json
from .discription import *
import scipy.stats as stats
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# Global variable for mapping cancer type to model
model_map = {
    'colorectal': ColorectalCancerData,
    'lung': LungCancerData,
    'breast': BreastCancerData,
    'prostate': ProstateCancerData,
    'gastric': GastricCancerData,
    # Add other cancer types here
}


def get_cancer_data(request, cancer_type):

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


def stats_data(request, cancer_type):
    
    if cancer_type not in model_map:
        return JsonResponse({'error': 'Invalid cancer type'}, status=400)
    
    model = model_map[cancer_type]
    data_query = model.objects.all().values()
    df = pd.DataFrame(data_query)

    dstat = get_descriptive_statistics(df)
    return JsonResponse(dstat.to_dict())


def get_descriptive_statistics(df, alter=3):
    """
    Calculate descriptive statistics for each column in the DataFrame.
    
    Parameters:
    df (pd.DataFrame): DataFrame containing the data.
    alter: drop numbers of start column and last one column; i.e. only select numeric; default will be 3 (id and country) and last cancer screening
    
    Returns:
    pd.DataFrame: DataFrame containing the descriptive statistics.
    """
    datavals = {}
    # Exclude first two columns (id and country) and last column if it's text (CANCER SCREENING)
    for i in range(df.shape[1]-alter): 
        data = df.iloc[:, (alter-1)+i].astype(float).to_list()
        datavals[df.iloc[:, (alter-1)+i].name] = {
            "mean": np.mean(data).__float__(),
            "median": np.median(data).__float__(),
            "std": np.std(data).__float__(),
            "variance": np.var(data).__float__(),
            "min": np.min(data).__float__(),
            "max": np.max(data).__float__(),
            "skew": stats.skew(data).__float__(),
            "kurtosis": stats.kurtosis(data).__float__(),
            "coefficient of variation": stats.variation(data).__float__(),
            "75th percentile": np.percentile(data, 75).__float__(),
            "50th percentile": np.percentile(data, 50).__float__(),
            "25th percentile": np.percentile(data, 25).__float__(),
            "interquartile range": stats.iqr(data).__float__(),
        }
    dstat = pd.DataFrame.from_dict(datavals, orient='index').transpose().transform(lambda x: x.round(3))
    # dstat = pd.read_json(dstat)
    return dstat