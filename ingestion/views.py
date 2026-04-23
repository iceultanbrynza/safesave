import json

from django.shortcuts import render, redirect
from rest_framework.request import Request
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from django.db import transaction

from .serializers import (AlarmIngestionSerializer,
                          EventIngestionSerializer,
                          RobotAddingSerializer,
                          EventAlarmSerializer)
from .models import Alarm
# Create your views here.

class PostAlarm(APIView):
    def post(self, request:Request, format=None):
        serializer1 = AlarmIngestionSerializer(data=request.data)
        serializer2 = EventAlarmSerializer(data=request.data)

        serializer1.is_valid()
        serializer2.is_valid()

        if serializer1.errors:
            return Response(serializer1.errors, status=400)

        if serializer2.errors:
            return Response(serializer2.errors, status=400)

        with transaction.atomic():
            serializer1.save()
            serializer2.save()
        return Response({"ok": True})

class PostEvent(APIView):
    def post(self, request:Request, format=None):
        serializer = EventIngestionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"ok": True})

        return Response(serializer.errors, status=400)

class PostRobot(APIView):
    def post(self, request:Request):
        serializer = RobotAddingSerializer(data=request.data,
                                           context={"request": request})

        if serializer.is_valid():
            serializer.save()
            response = redirect('profile')
            return response

        return Response(serializer.errors, status=400)

class AcknoledgeAlarm(APIView):
    def post(self, request: Request, id):
        alarm = Alarm.objects.get(id=id)
        if alarm.status == "RTN":
            serializer = EventAlarmSerializer(data={
                                                        "robot": f"{alarm.robot}",
                                                        "situation": "Acknowledged",
                                                        "status": "ACK"
                                                    })

        if serializer.is_valid():
            serializer.save()

        response = redirect('alarms')
        return response