from django.db import models

# Create your models here.

class Alarm(models.Model):

    class StatusEnum(models.TextChoices):

        ACTIVE = "Active"
        RTN = "RTN"
        ACK = "Acknowledged"

    class SituationEnum(models.TextChoices):

        FIRE = "Fire"
        EXPLOSION = "Explosion"
        LEAKAGE = "Leakage"

    robot = models.ForeignKey(
        "safeapp.Robot",
        on_delete=models.CASCADE,
        related_name="alarms"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(null=True, blank=True, max_length=20,  default=StatusEnum.ACTIVE)
    situation = models.CharField(null=True, blank=True, max_length=20, choices=SituationEnum.choices)

class Journal(models.Model):

    class SensorEnum(models.TextChoices):

        FLAME = "Flame", "Flame sensor"
        SOUND = "Sound", "Sound sensor"
        GAS = "Gas", "Gas sensor"

    class StatusEnum(models.TextChoices):

        ACTIVE = "Active"
        RTN = "RTN"
        ACK = "Acknowledged"

    class SituationEnum(models.TextChoices):

        FIRE = "Fire"
        EXPLOSION = "Explosion"
        LEAKAGE = "Leakage"

    robot = models.ForeignKey(
        "safeapp.Robot",
        on_delete=models.CASCADE,
        related_name="journal"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    value = models.FloatField(null=True, blank=True)
    sensor = models.CharField(null=True, blank=True, max_length=20, choices=SensorEnum.choices)
    situation = models.CharField(null=True, blank=True, max_length=20, default="")
    status =models.CharField(null=True, blank=True, max_length=20, default="")