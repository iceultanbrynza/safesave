import json

from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from .serializers import (AlarmIngestionSerializer,
                          EventIngestionSerializer,
                          RobotAddingSerializer)
# Create your views here.

class PostAlarm(APIView):
    def post(self, request:Request, format=None):
        serializer = AlarmIngestionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"ok": True})

        return Response(serializer.errors, status=400)

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
            return Response({"ok": True})

        return Response(serializer.errors, status=400)