from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.conf import settings
from .models import *
import pandas as pd
import numpy as np
import plotly.express as px # type: ignore
import plotly.graph_objects as go # type: ignore
from django.views.decorators.clickjacking import xframe_options_exempt




def Infra(request):
    if request.method == 'POST':
        selected_database = request.POST.get('cancerType')
        settings.CANCER_TYPES = selected_database
        print("settings.CANCER_TYPES:", settings.CANCER_TYPES)
    return render(request, 'base.htm')



def plot_choropleth_map(country, discription, spcCenter, orthographic=True):
    
    data = dict(type = 'choropleth', 
        # location: country col
        locations = country, 
                
        # over country names if country code; 'ISO-3' can be used
        locationmode = 'country names', 
                
        # colorscale can be added as per requirement 
        # colorscale = 'Viridis', 
                
        # text can be used as popup datapoints
        text = discription, 
        z = spcCenter, # data point
        colorscale = [[0, '#F7F1F8'], [1, '#5643D1']],
        # colour bar if needed
        # colorbar = {'title': 'Specialized Centers'}
        showscale = False,
        ) 
                
    layout = dict(geo ={'scope': 'world'}) 
    
    # passing data dictionary as a list 
    fig = go.Figure(data = [data], layout = layout)

    # fig.update_layout(title_text="title", title_x=.5)
    if orthographic:
        fig.update_geos(projection_type="orthographic", showland=True, landcolor="#ffffff",
            showocean=True, oceancolor="#fcf4d2", showcoastlines=True, coastlinecolor="#5743c8")
        fig.update_layout(height=600, width=700, margin={"r":0,"t":0,"l":0,"b":0})
    else:
        fig.update_geos(showland=True, landcolor="#ffffff",
            showocean=True, oceancolor="#fcf4d2", showcoastlines=True, coastlinecolor="#5743c8")
        fig.update_layout(height=400, width=800, margin={"r":0,"t":0,"l":0,"b":0}, dragmode=False)
    fig.update_traces(hovertemplate = "<span><b>%{location}: %{z}</b><br>%{text}</span><extra></extra>",)
    # plotting graph
    return fig.show(config={'displayModeBar': False})