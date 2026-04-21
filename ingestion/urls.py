from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('send_alarm/', view=views.PostAlarm.as_view(), name='send_alarm'),
    path('send_event/', view=views.PostEvent.as_view(), name='send_event'),
    path('post_robot/', view=views.PostRobot.as_view(), name='post_robot'),
]
