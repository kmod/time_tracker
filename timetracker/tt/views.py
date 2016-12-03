import collections
import datetime
import pytz

tz = pytz.timezone("US/Pacific")

from django.db.models import Max
from django.shortcuts import render, get_object_or_404, redirect
import django.utils.timezone

from .models import Log, LogDescription

# Create your views here.

# import django.utils.timezone
# django.utils.timezone.activate(

FORMAT = "%Y-%m-%dT%H:%M"

def get_latest_log():
    l = Log.objects.select_related("description").all().order_by('-end')[:1]
    if len(l):
        return l[0]
    return None

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
        start = datetime.datetime.strptime(request.POST['start'], FORMAT)
        start = django.utils.timezone.make_aware(start, tz)
        end = request.POST['end']
        end = datetime.datetime.strptime(request.POST['end'], FORMAT)
        end = django.utils.timezone.make_aware(end, tz)

        last = get_latest_log()
        if last and last.description == desc and last.end == start:
            last.end = end
            last.save()
        else:
            l = Log(description=desc, start=start, end=end)
            l.save()

        return redirect("/enter")

    start = Log.objects.all().aggregate(Max('end'))['end__max']
    if start is None:
        start = datetime.datetime.now()
    else:
        start = start.astimezone(tz)
    print(start, repr(start))

    context = dict(
            start=start.strftime(FORMAT),
            end=datetime.datetime.now().strftime(FORMAT),
    )
    return render(request, "tt/enter.html", context)

ProcessedLog = collections.namedtuple("ProcessedLog", ("id", "start", "end", "duration", "description"))

def list(request):
    print(Log.objects.all()[0].start)

    raw_logs = Log.objects.select_related("description").all().order_by('-end')[:10]
    logs = []
    for l in raw_logs:
        s = int((l.end - l.start).total_seconds())
        logs.append(ProcessedLog(
            l.id,
            l.start.astimezone(tz).strftime("%-I:%M %p"),
            l.end.astimezone(tz).strftime("%-I:%M %p"),
            "%s:%02d" % (s // 3600, (s // 60) % 60),
            l.description.title))

    context = dict(
            logs=logs,
    )
    return render(request, "tt/list.html", context)

def delete(request, log_id):
    p = get_object_or_404(Log, pk=log_id)
    if request.method == "POST":
        p.delete()
        return redirect("/")

    return render(request, "tt/delete.html", {})
