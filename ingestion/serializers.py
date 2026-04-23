from rest_framework import serializers
from .models import Alarm, Journal
from safeapp.models import Robot

class AlarmIngestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alarm
        fields = ["robot", "situation", "status"]

class EventIngestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = ["robot", "value", "sensor"]

class EventAlarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = ["robot", "situation", "status"]

class RobotAddingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Robot
        fields = ["id", "name"]

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["owner"] = request.user
        return super().create(validated_data)

# class AcknowledgeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Alarm
#         fields = ['status']

#     def update(self, instance: Alarm, validated_data):
#         instance.status = validated_data.get('status', instance.status)
#         instance.save()
#         return instance