from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import localtime, now

class ScheduleCredentials(models.Model):
    '''
    One profile per user. Contains information not contained within
    user object.
    '''
    # this exists in case we want to add more fields e.g. bio, birthday
    username = models.CharField(max_length=30, null=True)
    password = models.CharField(max_length=30, null=True)