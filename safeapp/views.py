from django.shortcuts import render, redirect
from django.http import HttpRequest

from .models import Robot
from ingestion.models import Alarm, Journal
from django.contrib.auth.decorators import login_required

from uuid import UUID
# Create your views here.

def RequestHomePage(request):
    return render(request, "home/home.html")

@login_required
def RequestProfilePage(request):
    return render(request, "home/profile.html")

@login_required
def RequestAlarmsPage(request: HttpRequest):

    user = request.user
    robots = Robot.objects.filter(owner=user)

    try:
        robot_id = UUID(request.session.get("robot_id"))
    except:
        robot_id=None

    alarms = None
    if robot_id:
        alarms = Alarm.objects.filter(robot_id=robot_id)

    context = {
        "alarms": alarms,
        "robots": robots,
        "selected": robot_id
    }
    return render(request, "home/alarms.html", context=context)

@login_required
def RequestJournalPage(request: HttpRequest):
    user = request.user
    robots = Robot.objects.filter(owner=user)

    try:
        robot_id = UUID(request.session.get("robot_id"))
    except:
        robot_id=None

    events = None

    if robot_id:
        events = Journal.objects.filter(robot_id=robot_id)

    context = {
        "robots": robots,
        "events": events,
        "selected": robot_id
    }
    return render(request, "home/journal.html", context=context)

@login_required
def PostSelectedRobot(request: HttpRequest):
    if request.method == "POST":
        robot_id = request.POST.get("robot_id")

        request.session["robot_id"] = robot_id

        source = request.GET.get('next')

    return redirect(f"/{source}")