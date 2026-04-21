from django.db import models
from roles.models import User
import uuid
# Create your models here.

class Robot(models.Model):

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="robots",
        null=True,
        blank=True
    )

    id = models.UUIDField(primary_key=True, editable=True)
    name = models.CharField(max_length=100,null=True, blank=True)
