import time
import urllib

from django.db.models import Max
from django.shortcuts import render, get_object_or_404, redirect

from .models import Log, LogDescription

# Create your views here.

# import django.utils.timezone
# django.utils.timezone.activate(

def enter(request):
    if request.method == "POST":
        pass
    start = Log.objects.all().aggregate(Max('end'))['end__max']
    if start is None:
        start = time.localtime()
    print(start)
    context = dict(
            start=time.strftime("%Y-%m-%dT%H:%M:%S", start),
            end=time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime()),
    )
    return render(request, "tt/enter.html", context)
