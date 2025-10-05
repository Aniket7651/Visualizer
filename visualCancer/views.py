from django.conf import settings
from django.shortcuts import render
from django_pandas.io import read_frame # type: ignore
import pandas as pd
import io, base64, json, os
import matplotlib.pyplot as plt
from .api import get_descriptive_statistics, OverAllAvg_statDF
from django.http import FileResponse, HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from .models import BreastCancerData, LungCancerData, ColorectalCancerData, ProstateCancerData, GastricCancerData, AverageValues, OverviewDetails
from .discription import *


def downloadPolicy_file(request, cancer_type, country):
    # file_path = f"Data/{cancer_type.title()}PolicyPaper/{country} - {cancer_type.title()} Cancer Policy.pdf"
    cancer_type = cancer_type.title()
    if cancer_type == "Prostate":
        cancer_type_wrong_spell = "Protest"

    else:
        cancer_type_wrong_spell = cancer_type

    country = country.title()
    file_path = os.path.join(settings.MEDIA_ROOT, 'Data', f"{cancer_type}PolicyPaper", f"{country} - {cancer_type_wrong_spell} Cancer Policy.pdf")
    # print(file_path)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    else: 
        return HttpResponse(f"<h1>Policy Paper file not found for {country} - {cancer_type} Cancer</h1>", status=404)


def downloadFactSheet_file(request, cancer_type, country):
    # file_path = f"Data/{cancer_type.title()}PolicyPaper/{country} - {cancer_type.title()} Cancer Policy.pdf"
    cancer_type = cancer_type.title()
    country = country.title()

    if cancer_type == "Lung":
        if os.path.exists(os.path.join(settings.MEDIA_ROOT, 'Data', f'{cancer_type}FactSheet', country, f"{country}- {cancer_type} Cancer.pdf")):
            fileName = f"{country}- {cancer_type} Cancer.pdf"
        else:
            fileName = f"{country}-{cancer_type}Cancer.pdf"


    elif cancer_type == "Breast":
        fileName = f"Factsheet - {country} High Resolution SWOT.pdf" # Factsheet - Algeria High Resolution SWOT

    elif cancer_type == "Gastric":
        if os.path.exists(os.path.join(settings.MEDIA_ROOT, 'Data', f'{cancer_type}FactSheet', country, f"{country} - {cancer_type} Cancer High Resolution.pdf")):
            fileName = f"{country} - {cancer_type} Cancer High Resolution.pdf"
        else: 
            fileName = f"{country} - Gastric Cancer High Resolution.pdf"

    elif cancer_type == "Prostate":
        if os.path.exists(os.path.join(settings.MEDIA_ROOT, 'Data', f'{cancer_type}FactSheet', country, f"{country} - {cancer_type} Cancer High Resolution.pdf")):
            fileName = f"{country} - {cancer_type} Cancer High Resolution.pdf"
        
        else:
            fileName = f"{country} - {cancer_type.lower()} cancer High Resolution.pdf"
    elif cancer_type == "Colorectal":
        if os.path.exists(os.path.join(settings.MEDIA_ROOT, 'Data', f'{cancer_type}FactSheet', country, f"{country} - {cancer_type} Cancer High Resolution.pdf")):
            fileName = f"{country} - {cancer_type} Cancer High Resolution.pdf"
        else:
            fileName = f"{country} - High Resolution {cancer_type} Cancer.pdf"


    file_path = os.path.join(settings.MEDIA_ROOT, 'Data', f'{cancer_type}FactSheet', country, fileName)
    print(file_path)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    else:
        return HttpResponse(f"<h1>Fact Sheet file not found for {country} - {cancer_type} Cancer</h1>", status=404)



def dataframe_to_column_json(df):
    """
    Converts a Pandas DataFrame to a JSON object where each column's data is stored separately.
    Args:
        df (pd.DataFrame): Input DataFrame with columns like 'country', 'Specialized_Center', etc.
    Returns:
        dict: JSON-compatible dict with columns and their data lists.
    """
    charts_data = []
    for col in df.columns:
        column_data = {
            'column_name': col,
            'data': df[col].to_list()
        }
        charts_data.append(column_data)
    
    json_data = json.dumps(charts_data)

    return json_data


def DataSet_to_JSON_Avg_for_BoxPlot(df, cancer_type):
    data = df[df['cancer_type'] == cancer_type.title()].set_index('country')
    data = data.drop(['id', 'cancer_type'], axis=1)
    chart_data = []
    for col in data.columns:
        dict_data = {
            'y': data[col].to_list(),
            'name': col.replace('_', ' ').title(),
            'boxpoints': 'all',
            'jitter': 0.3,
            'pointpos': -1.8,
            'type': 'box',
            'marker': {'color': '#f3c750'}
        }
        chart_data.append(dict_data)
    return json.dumps(chart_data)


# Views for the visualCancer app
def index(request):
    textContext = {}
    
    return render(request, 'index.html', textContext)


def apiAccess(request):
    return render(request, 'apiAccess.html')


def overviewPage(request, cancer_type, country):
    context = {}
    try:
        OverviewDetails_obj = OverviewDetails.objects.get(cancer_type=cancer_type, country=country.title())

        context['cancer_type'] = OverviewDetails_obj.cancer_type.title()
        context['country'] = OverviewDetails_obj.country
        context['country_shortForm'] = OverviewDetails_obj.country_shortForm
        context['introduction'] = OverviewDetails_obj.introduction
        context['swot_analysis'] = OverviewDetails_obj.swot_analysis
        context['infrastructure'] = OverviewDetails_obj.infrastructure
        context['treatment_funding_awareness'] = OverviewDetails_obj.treatment_funding_awareness
        context['survival_rates'] = OverviewDetails_obj.survival_rates
        context['biomarkers'] = OverviewDetails_obj.biomarkers
        context['clinical_guidelines'] = OverviewDetails_obj.clinical_guidelines
        context['reimbursement'] = OverviewDetails_obj.reimbursement
        context['cancer_screening'] = OverviewDetails_obj.cancer_screening

        return render(request, 'overview.html', context)
    
    except OverviewDetails.DoesNotExist:
        context['cancer_type'] = cancer_type.title()
        context['country'] = country.title()
        
        return render(request, 'notfound.html', context)

    


def datasetView(request):
    
    df = pd.DataFrame(LungCancerData.objects.all().values())
    ovaDF = pd.DataFrame(AverageValues.objects.all().values())
    stat = get_descriptive_statistics(df)
    countryStat = OverAllAvg_statDF('lung')

    context = {
        'table': df.to_html(classes='dataframe', index=False),
        'heading': 'Lung Cancer Data',
        'des_stat': stat.to_html(classes='statframe'),
        'chart_data': dataframe_to_column_json(stat),
        'countryWise_stat': countryStat.to_html(classes='statframe'),
        'boxPlot_data': DataSet_to_JSON_Avg_for_BoxPlot(ovaDF, 'lung'),
    }
    
    cancer_type = request.GET.get('cancerType', 'lung')

    if cancer_type == 'breast':
        df = pd.DataFrame(BreastCancerData.objects.all().values())
    elif cancer_type == 'lung':
        df = pd.DataFrame(LungCancerData.objects.all().values())
    elif cancer_type == 'colorectal':
        df = pd.DataFrame(ColorectalCancerData.objects.all().values())
    elif cancer_type == 'prostate':
        df = pd.DataFrame(ProstateCancerData.objects.all().values())
    elif cancer_type == 'gastric':
        df = pd.DataFrame(GastricCancerData.objects.all().values())
    else:
        context['table'] = None
        context['des_stat'] = None
        context['heading'] = "No data available for the selected cancer type."
    
    stat = get_descriptive_statistics(df)
    countryStat = OverAllAvg_statDF(cancer_type)
    context['des_stat'] = stat.to_html(classes='statframe')
    context['table'] = df.to_html(classes='dataframe', index=False)
    context['heading'] = 'Breast Cancer Data'
    context['chart_data'] = dataframe_to_column_json(stat)
    context['countryWise_stat'] = countryStat.to_html(classes='statframe')
    context['boxPlot_data'] = DataSet_to_JSON_Avg_for_BoxPlot(ovaDF, cancer_type)

    return render(request, 'data.html', context)


def plot_generator(column_, title, xlabel='Date', ylabel='Value', kind='bar'):
    column_.plot(kind=kind, figsize=(10, 5), title=title, xlabel=xlabel, ylabel=ylabel)

    # Save plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close() # Close the plot to free memory

    # Encode the image to base64
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return image_base64


def view_feedback(request):
    if request.method == 'POST':

        name = request.POST.get('name')
        email = request.POST.get('email')
        country = request.POST.get('country')
        affilation = request.POST.get('role')
        profession = request.POST.get('profession')
        Feedback_msg = request.POST.get('feedback')

        # Save feedback to the database
        from .models import Feedback
        feedback_entry = Feedback(
            name=name,
            email=email,
            country=country,
            affiliation=affilation,
            profession=profession,
            feedback_type="General",
            comments=Feedback_msg
        )
        feedback_entry.save()

        return render(request, 'feedback.html', {
            'success_message': "“Thank you for contributing to ICPC. Your perspective helps shape the next updates of our factsheets, policy papers, and global equity index.”"
        })
    return render(request, 'feedback.html')


def view_methodology(request):
    return render(request, 'methodology.html')
