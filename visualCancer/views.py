from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.conf import settings
from .models import *
from django.views.decorators.clickjacking import xframe_options_exempt


def Index(request, pagetitle='Home'):
    return render(request, 'Index.htm', {'title': pagetitle})