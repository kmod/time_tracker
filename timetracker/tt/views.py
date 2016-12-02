import time
import urllib

from django.shortcuts import render, get_object_or_404, redirect

from .models import Log, LogDescription

# Create your views here.

# import django.utils.timezone
# django.utils.timezone.activate(

def enter(request):
    context = dict(
            start="12:00:00",
            end=time.strftime("%H:%M:%S", time.localtime()),
    )
    return render(request, "tt/enter.html", context)
