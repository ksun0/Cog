from Dashboard.models import *
from django.db import models
import sys
import os

class CalendarList(models.Model):
    '''
    A list of synced calendars within a single account.
    '''
    #TO-DO: Add CanMultitask boolean
    profile = models.ForeignKey(User, on_delete=models.CASCADE)
    account_id = models.CharField(max_length=70, unique=True)

class Calendar(models.Model):
    '''
    A calendar.
    '''
    title = models.CharField(max_length=200, unique=True)
    cal_id = models.CharField(max_length=200)
    handler = models.ForeignKey(CalendarList, on_delete=models.CASCADE)


class CredentialsModel(models.Model):
    # Google Credentials
    id = models.OneToOneField(User, primary_key=True)
    calList = models.OneToOneField(CalendarList, null=True)
    credential = CredentialsField()