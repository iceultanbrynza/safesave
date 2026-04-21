from rest_framework import serializers
from .models import Alarm, Journal
from safeapp.models import Robot

class AlarmIngestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alarm
        fields = ["robot", "situation"]

class EventIngestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = ["robot", "value", "sensor"]

class RobotAddingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Robot
        fields = ["id", "name"]

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["owner"] = request.user
        return super().create(validated_data)
