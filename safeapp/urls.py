from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', view=views.RequestHomePage, name='home'),
    path('alarms/', view=views.RequestAlarmsPage, name='alarms'),
    path('journal/', view=views.RequestJournalPage, name='journal'),
    path('select_robot/', view=views.PostSelectedRobot, name='select_robot'),
    path('profile/', view=views.RequestProfilePage, name='profile'),
]
