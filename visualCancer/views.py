from django.shortcuts import render
from django_pandas.io import read_frame # type: ignore
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import BreastCancerData, LungCancerData, ColorectalCancerData, ProstateCancerData, GastricCancerData
from .discription import *

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