from django.contrib import admin
from .models import Alarm, Journal
# Register your models here.

admin.site.register([Alarm, Journal])