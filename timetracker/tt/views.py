import collections
import datetime

from django.db.models import Max
from django.shortcuts import render, get_object_or_404, redirect

from .models import Log, LogDescription

# Create your views here.

# import django.utils.timezone
# django.utils.timezone.activate(

FORMAT = "%Y-%m-%dT%H:%M"

def enter(request):
    if request.method == "POST":
        assert request.POST["description"]
        assert request.POST["start"]
        assert request.POST["end"]

        try:
            desc = LogDescription.objects.get(title=request.POST['description'].strip())
        except LogDescription.DoesNotExist:
            desc = LogDescription(title=request.POST['description'].strip())
        desc.save()

        start = request.POST['start']
        print(start)
        start = datetime.datetime.strptime(request.POST['start'], FORMAT)
        print(start)
        end = request.POST['end']
        print(end)
        end = datetime.datetime.strptime(request.POST['end'], FORMAT)
        print(end)
        l = Log(description=desc, start=start, end=end)
        l.save()
        print(l.start)

        return redirect("/enter")

    start = Log.objects.all().aggregate(Max('end'))['end__max']
    if start is None:
        start = datetime.datetime.now()
    else:
        start = start.astimezone(None)
    print(start, repr(start))

    context = dict(
            start=start.strftime(FORMAT),
            end=datetime.datetime.now().strftime(FORMAT),
    )
    return render(request, "tt/enter.html", context)

ProcessedLog = collections.namedtuple("ProcessedLog", ("start", "end", "duration", "description"))

def list(request):
    print(Log.objects.all()[0].start)

    raw_logs = Log.objects.select_related("description").all().order_by('-end')[:10]
    logs = []
    for l in raw_logs:
        logs.append(ProcessedLog(
            l.start.astimezone(None).strftime("%-I:%M %p"),
            l.end.astimezone(None).strftime("%-I:%M %p"),
            l.end - l.start,
            l.description.title))

    context = dict(
            logs=logs,
    )
    return render(request, "tt/list.html", context)
