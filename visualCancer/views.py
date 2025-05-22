# views.py
from django.shortcuts import render
from django_pandas.io import read_frame # type: ignore
import pandas as pd
import numpy as np
import plotly.graph_objects as go # type: ignore
import plotly.offline as opy # type: ignore
from plotly import express as px # type: ignore
from .models import BreastCancerData, LungCancerData, ColorectalCancerData, ProstateCancerData
from .discription import *

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


def histogramChart(df, x, y):
    fig = px.histogram(
        df,
        x=x,
        y=y
    )
    fig.update_traces(marker_color='#f3c750')
    fig.update_layout(height=500)
    # Show the plot
    html_fig = opy.plot(fig, auto_open=False, output_type='div', config={'displayModeBar': False})
    return html_fig


def Infra(request):
    # Default context
    context = {'geomap': None, 'ubmap': None, 'csmap': None, 'trmap': None, 'sepmap': None,
               'avgmap': None, 
               'map_type': 'br_sc', 'ubmap_type': 'her2',
               'cancer_type': 'BreastCancer',
               'content': None,
               'head': None,
               'biomarker_btn': zip(brst_BioMBtnValue, brst_BioMBtnName)}

    # Handle POST request (cancer type selection)
    if request.method == 'POST':
        selected_database = request.POST.get('cancerType', 'BreastCancer')
        context['cancer_type'] = selected_database
    else:
        selected_database = 'BreastCancer'  # Default for GET requests

    # Load data
    try:
        df = read_frame(BreastCancerData.objects.all())

        if context['cancer_type'] == 'BreastCancer':
            df = read_frame(BreastCancerData.objects.all())
            context['head'] = BreastHeading
            context['content'] = BreastCancer_cont
            context['biomarker_btn'] = zip(brst_BioMBtnValue, brst_BioMBtnName)
        
        # elif context['cancer_type'] == 'LungCancer':

        if df.empty:
            context['geomap'] = "<div>No data available</div>"
            return render(request, 'Visualizer.html', context)

    except Exception as e:
        context['geomap'] = "<div>Error loading data</div>"
        return render(request, 'Visualizer.html', context)

    # Handle infra map type (GET parameter)
    map_type = request.GET.get('map_type', 'br_sc')
    context['map_type'] = map_type

    if map_type == 'br_gm':
        df['discription'] = df['GeneMol_Centers'].apply(lambda x: discLoader(brst_Infra_discription, x))
        # Map 2: Genetic & Molecular Testing
        gm_div = plot_choropleth_map(
            df['country'].values,
            df['discription'].values,
            df['GeneMol_Centers'].values,
            orthographic=False
        )
        context['avgmap'] = histogramChart(df, df['country'].values, df['Infra_Avg'].values)
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
        context['avgmap'] = histogramChart(df, df['country'].values, df['Infra_Avg'].values)

    # Handle biomarker map type (GET parameter)
    ubmap_type = request.GET.get('ubmap_type', 'her2')
    context['ubmap_type'] = ubmap_type

    if ubmap_type == 'brac1':
        df['discription'] = df['BRAC1'].apply(lambda x: discLoader(brst_ubiom_discription, x))
        # Map 1: BRCA1
        brca1_div = plot_choropleth_map(
            df['country'].values,
            df['discription'].values,
            df['BRAC1'].values,
            orthographic=False
        )
        context['avgmap'] = histogramChart(df, df['country'].values, df['Biomark_Avg'].values)
        context['ubmap'] = brca1_div

    elif ubmap_type == 'er':
        df['discription'] = df['ER'].apply(lambda x: discLoader(brst_ubiom_discription, x))
        # Map 2: ER
        er_div = plot_choropleth_map(
            df['country'].values,
            df['discription'].values,
            df['ER'].values,
            orthographic=False
        )
        context['avgmap'] = histogramChart(df, df['country'].values, df['Biomark_Avg'].values)
        context['ubmap'] = er_div

    elif map_type == 'pr':
        df['discription'] = df['PR'].apply(lambda x: discLoader(brst_ubiom_discription, x))
        # Map 3: PR
        pr_div = plot_choropleth_map(
            df['country'].values,
            df['discription'].values,
            df['PR'].values,
            orthographic=False
        )
        context['avgmap'] = histogramChart(df, df['country'].values, df['Biomark_Avg'].values)
        context['ubmap'] = pr_div

    else:
        df['discription'] = df['HER2'].apply(lambda x: discLoader(brst_ubiom_discription, x))
        # Map DEFAULT: HER2
        HER2_div = plot_choropleth_map(
            df['country'].values,
            df['discription'].values,
            df['HER2'].values,
            orthographic=False
        )
        context['avgmap'] = histogramChart(df, df['country'].values, df['Biomark_Avg'].values)
        context['ubmap'] = HER2_div
    

    return render(request, 'Visualizer.html', context)