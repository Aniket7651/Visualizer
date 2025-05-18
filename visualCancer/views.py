# views.py
from django.shortcuts import render
from django_pandas.io import read_frame # type: ignore
import pandas as pd
import numpy as np
import plotly.graph_objects as go # type: ignore
import plotly.offline as opy # type: ignore
from .models import BreastCancerData
from .discription import brst_Infra_discription

def discLoader(dict, num):
    for key, value in dict.items():
        if key == num:
            return value

def plot_choropleth_map(country, discription, spcCenter, orthographic=False):
    # Check for empty or invalid data
    if not country.size or not discription.size or not spcCenter.size:  # Use .size to check array length
        return "<div>No data available for map</div>"

    # Ensure arrays are not all NaN or invalid
    if np.all(pd.isna(country)) or np.all(pd.isna(discription)) or np.all(pd.isna(spcCenter)):
        print("Error: All data is NaN or invalid")
        return "<div>Invalid data for map</div>"

    data = dict(
        type='choropleth',
        locations=country,
        locationmode='country names',
        text=discription,
        z=spcCenter,
        colorscale=[[0, '#F7F1F8'], [1, '#5643D1']],
        showscale=False,
    )

    layout = dict(geo={'scope': 'world'})

    fig = go.Figure(data=[data], layout=layout)

    if orthographic:
        fig.update_geos(projection_type="orthographic", showland=True, landcolor="#ffffff",
            showocean=True, oceancolor="#fcf4d2", showcoastlines=True, coastlinecolor="#5743c8")
        fig.update_layout(height=650, margin={"r":0,"t":0,"l":0,"b":0})
    else:
        fig.update_geos(showland=True, landcolor="#ffffff",
            showocean=True, oceancolor="#fcf4d2", showcoastlines=True, coastlinecolor="#5743c8")
        fig.update_layout(height=650, margin={"r":0,"t":0,"l":0,"b":0}, dragmode=False)
    fig.update_traces(hovertemplate="<span><b>%{location}: %{z}</b><br>%{text}</span><extra></extra>")

    html_fig = opy.plot(fig, auto_open=False, output_type='div', config={'displayModeBar': False})
    return html_fig


def Infra(request):
    # Default context
    context = {'geomap': None, 'map_type': 'sc', 'cancer_type': 'BreastCancer'}

    # Handle POST request (cancer type selection)
    if request.method == 'POST':
        selected_database = request.POST.get('cancerType', 'BreastCancer')
        context['cancer_type'] = selected_database
    else:
        selected_database = 'BreastCancer'  # Default for GET requests

    # Load data
    try:
        df = read_frame(BreastCancerData.objects.all())
        if df.empty:
            context['geomap'] = "<div>No data available</div>"
            return render(request, 'base.htm', context)
        
    except Exception as e:
        context['geomap'] = "<div>Error loading data</div>"
        return render(request, 'base.htm', context)

    # Handle map type (GET parameter)
    map_type = request.GET.get('map_type', 'sc')
    context['map_type'] = map_type

    if map_type == 'gm':
        df['discription'] = df['GeneMol_Centers'].apply(lambda x: discLoader(brst_Infra_discription, x))
        # Map 2: Genetic & Molecular Testing
        gm_div = plot_choropleth_map(
            df['country'].values,
            df['discription'].values,
            df['GeneMol_Centers'].values,
            orthographic=False
        )
        context['geomap'] = gm_div
    else:
        df['discription'] = df['Specialized_Centers'].apply(lambda x: discLoader(brst_Infra_discription, x))
        # Map 1: Specialized Centers
        sc_div = plot_choropleth_map(
            df['country'].values,
            df['discription'].values,
            df['Specialized_Centers'].values,
            orthographic=False
        )
        context['geomap'] = sc_div

    return render(request, 'base.htm', context)