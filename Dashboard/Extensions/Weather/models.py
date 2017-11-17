from Dashboard.models import *
from django.db import models
import sys
import os

class WeatherModel(models.Model):
    '''
    Store the weather.
    '''
    temperature = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    extension_id = models.UUIDField(editable=False, null=True)
