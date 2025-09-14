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


def download_file(request, cancer_type, country):
    # file_path = f"Data/{cancer_type.title()}PolicyPaper/{country} - {cancer_type.title()} Cancer Policy.pdf"
    cancer_type = cancer_type.title().replace(" ", "_")
    if cancer_type == "Prostate":
        cancer_type_wrong_spell = "Protest"

    else:
        cancer_type_wrong_spell = cancer_type

    country = country.title().replace(" ", "_")
    file_path = os.path.join(settings.MEDIA_ROOT, 'Data', f"{cancer_type}PolicyPaper", f"{country} - {cancer_type_wrong_spell} Cancer Policy.pdf")
    print(file_path)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    else: 
        return HttpResponse(f"Policy Paper file not found for {country} - {cancer_type}", status=404)


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











def discLoader(dict, num):
    for key, value in dict.items():
        if key == num:
            return value
    return "No description available"

@require_GET
def get_map_data(request):
    map_type = request.GET.get('map_type', 'br_sc')
    cancer_type = request.GET.get('cancer_type', 'BreastCancer')

    try:
        if cancer_type == 'BreastCancer':
            df = read_frame(BreastCancerData.objects.all())
            discription_dict = brst_Infra_discription if map_type in ['br_sc', 'br_gm'] else brst_ubiom_discription
        elif cancer_type == 'LungCancer':
            df = read_frame(LungCancerData.objects.all())
            discription_dict = brst_Infra_discription if map_type in ['br_sc', 'br_gm'] else lung_ubiom_discription
        elif cancer_type == 'ColorectalCancer':
            df = read_frame(ColorectalCancerData.objects.all())
            discription_dict = colorectal_Infra_discription if map_type in ['br_sc', 'br_gm'] else colorectal_ubiom_discription
        elif cancer_type == 'ProstateCancer':
            df = read_frame(ProstateCancerData.objects.all())
            discription_dict = prostate_Infra_discription if map_type in ['br_sc', 'br_gm'] else prostate_ubiom_discription
        elif cancer_type == 'GastricCancer':
            df = read_frame(GastricCancerData.objects.all())
            discription_dict = gastric_Infra_discription if map_type in ['br_sc', 'br_gm'] else gastric_ubiom_discription
        else:
            return JsonResponse({'error': 'Invalid cancer type'}, status=400)

        if df.empty:
            return JsonResponse({'error': 'No data available'}, status=400)

        if map_type == 'br_sc':
            df['discription'] = df['Specialized_Centers'].apply(lambda x: discLoader(discription_dict, x))
            data = {
                'countries': df['country'].tolist(),
                'descriptions': df['discription'].tolist(),
                'values': df['Specialized_Centers'].tolist()
            }
        elif map_type == 'br_gm':
            df['discription'] = df['GeneMol_Centers'].apply(lambda x: discLoader(discription_dict, x))
            data = {
                'countries': df['country'].tolist(),
                'descriptions': df['discription'].tolist(),
                'values': df['GeneMol_Centers'].tolist()
            }
        elif map_type == 'her2':
            df['discription'] = df['HER2'].apply(lambda x: discLoader(discription_dict, x))
            data = {
                'countries': df['country'].tolist(),
                'descriptions': df['discription'].tolist(),
                'values': df['HER2'].tolist()
            }
        elif map_type == 'brac1':
            df['discription'] = df['BRAC1'].apply(lambda x: discLoader(discription_dict, x))
            data = {
                'countries': df['country'].tolist(),
                'descriptions': df['discription'].tolist(),
                'values': df['BRAC1'].tolist()
            }
        elif map_type == 'er':
            df['discription'] = df['ER'].apply(lambda x: discLoader(discription_dict, x))
            data = {
                'countries': df['country'].tolist(),
                'descriptions': df['discription'].tolist(),
                'values': df['ER'].tolist()
            }
        elif map_type == 'pr':
            df['discription'] = df['PR'].apply(lambda x: discLoader(discription_dict, x))
            data = {
                'countries': df['country'].tolist(),
                'descriptions': df['discription'].tolist(),
                'values': df['PR'].tolist()
            }
        else:
            return JsonResponse({'error': 'Invalid map type'}, status=400)

        return JsonResponse(data)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_GET
def get_histogram_data(request):
    map_type = request.GET.get('map_type', 'br_sc')
    cancer_type = request.GET.get('cancer_type', 'BreastCancer')

    try:
        if cancer_type == 'BreastCancer':
            df = read_frame(BreastCancerData.objects.all())
        elif cancer_type == 'LungCancer':
            df = read_frame(LungCancerData.objects.all())
        elif cancer_type == 'ColorectalCancer':
            df = read_frame(ColorectalCancerData.objects.all())
        elif cancer_type == 'ProstateCancer':
            df = read_frame(ProstateCancerData.objects.all())
        else:
            return JsonResponse({'error': 'Invalid cancer type'}, status=400)

        if df.empty:
            return JsonResponse({'error': 'No data available'}, status=400)

        if map_type in ['br_sc', 'br_gm']:
            data = {
                'x': df['country'].tolist(),
                'y': df['Infra_Avg'].tolist()
            }
        elif map_type in ['her2', 'brac1', 'er', 'pr']:
            data = {
                'x': df['country'].tolist(),
                'y': df['Biomark_Avg'].tolist()
            }
        else:
            return JsonResponse({'error': 'Invalid map type'}, status=400)

        return JsonResponse(data)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



def Infra(request):
    context = {
        'map_type': 'br_sc',
        'ubmap_type': 'her2',
        'cancer_type': 'BreastCancer',
        'content': None,
        'head': None,
        'biomarker_btn': zip(brst_BioMBtnValue, brst_BioMBtnName)
    }

    selected_database = request.POST.get('cancerType', 'BreastCancer') if request.method == 'POST' else 'BreastCancer'
    context['cancer_type'] = selected_database

    try:
        if selected_database == 'BreastCancer':
            df = read_frame(BreastCancerData.objects.all())
            context['head'] = BreastHeading
            context['content'] = BreastCancer_cont
            context['biomarker_btn'] = zip(brst_BioMBtnValue, brst_BioMBtnName)
            
        elif selected_database == 'LungCancer':
            df = read_frame(LungCancerData.objects.all())
            context['head'] = LungHeading
            context['content'] = LungCancer_cont
            context['biomarker_btn'] = zip(lung_BioMBtnValue, lung_BioMBtnName)

        elif selected_database == 'ColorectalCancer':
            df = read_frame(ColorectalCancerData.objects.all())
            context['head'] = ColorectalHeading
            context['content'] = ColorectalCancer_cont
            context['biomarker_btn'] = zip(colorectal_BioMBtnValue, colorectal_BioMBtnName)

        elif selected_database == 'ProstateCancer':
            df = read_frame(ProstateCancerData.objects.all())
            context['head'] = ProstateHeading
            context['content'] = ProstateCancer_cont
            context['biomarker_btn'] = zip(prostate_BioMBtnValue, prostate_BioMBtnName)
        else:
            return render(request, 'Visualizer.html', context)

        if df.empty:
            return render(request, 'Visualizer.html', context)

    except Exception as e:
        print(f"Error in Infra view: {e}")
        return render(request, 'Visualizer.html', context)

    return render(request, 'Visualizer.html', context)