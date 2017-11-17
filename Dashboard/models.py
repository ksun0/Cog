from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import localtime, now
import uuid
import datetime
from decimal import Decimal
import json
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from oauth2client.contrib.django_util.models import CredentialsField
from math import sqrt
import logging
from .Extension_Models import *
import glob2
from importlib import import_module

class Profile(models.Model):
    '''
    One profile per user. Contains information not contained within
    user object.
    '''
    # this exists in case we want to add more fields e.g. bio, birthday
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True) #null=True is probs not good practice but it fixes an error
    description = models.CharField(max_length=600, null=True)


    def __str__(self):
        if self.user:
            return self.user.username
        else:
            return "there's a null user here..."

class EventManager(models.Manager):
    '''
    Manager for events.
    TO-DO: Add more detailed comment.
    '''
    def get_queryset(self):
        return super(EventManager, self).get_queryset()

    def get_todays_events(self):
        today_start = localtime(now()).replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timezone.timedelta(days=1)
        return super(EventManager, self).get_queryset().filter(end_time__gte=today_start, start_time__lte=today_end)

class Event(models.Model):
    '''
    Represents a job that has a defined time.
    '''
    #TO-DO: Add CanMultitask boolean
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now) # may need to be timezone.now

    start_time = models.DateTimeField('start time', null=True)
    end_time = models.DateTimeField('end time', null=True)

    # override default manager
    objects = EventManager()
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    extension_id = models.UUIDField(editable=False, null=True)

    def __str__(self):
        return json.dumps({"Title": self.title,
                           "Description": self.description,
                           "Start Time": str(self.start_time),
                           "End Time": str(self.end_time),
                           "Creation Date": str(self.created_at),
                           "unique_id": str(self.unique_id)})

class Unit(models.Model):
    '''
    Represents a job that has no defined time, though may have
    a due date.
    per_unit: the ratio of the unit per time. Like pages per minute
    num_used: The number of people that have used this unit. Used in
    update calculation.
    '''
    title = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=200)
    profile_id = models.IntegerField() # profile id = 0 --> default unit
    ratio = models.FloatField()

    # Welford's method for measuring standard deviation
    # Used to find outliers.
    # https://stackoverflow.com/questions/895929/how-do-i-determine-the-standard-deviation-stddev-of-a-set-of-values
    M = models.FloatField(default=0.0) # -1 if static variable. Like Hours.
    S = models.FloatField(default=0.0)
    k = models.IntegerField(default=1)
    time_sum = models.FloatField(default=0.0) # Used for calculating mean

    def __str__(self):
        return self.title

    def get_standard_deviation(self):
        return sqrt(self.S / (self.k-2));

    def update_ratio(self, value):
        # If this unit has been used less than 10 times or
        # the new value is within the std
        num_cases = self.k-1
        num_entries_before_filtering = 10
        if self.k >= num_entries_before_filtering:
            mean = self.time_sum/(num_cases)
            sd = self.get_standard_deviation()
        # If k == -1, then it's a static unit. Like Hours or Minutes
        # If it's non-static and it either not filtering yet or within
        # the filter, then update
        if self.k != -1 and\
            (self.k < num_entries_before_filtering or
                        (value > mean - 3 * sd and \
                                value < mean + 3 * sd)):
            tmpM = self.M
            self.M += (value - tmpM) / self.k;
            self.S += (value - tmpM) * (value - self.M)
            self.k += 1
            self.time_sum += value
            print("HERE?")
            self.ratio = (self.ratio+value)/(num_cases+1)
        else:
            logging.info("Tried adding outside std: " + str(value) + " at k="+ str(self.k)+" sd="+str(sd)+" mean="+str(mean))

class Task(models.Model):
    '''
    A job with a predefined length.
    '''
    # DO NOT USE THE DEFAULT INIT!!!!!!!! USE CREATE!!!!!!!!!!
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now) # may need to be timezone.now

    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    # characteristic_number like pages, questions, etc.
    c_number = models.DecimalField(max_digits=8, decimal_places=2, null=True) # note: make sure null=True doesn't cause problems
    priority = models.IntegerField()
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)

    def __str__(self):
        return json.dumps({"Title": self.title,
                           "Priority": self.priority,
                           "Description": self.description,
                           "Total Time": str(int(float(self.c_number)*self.unit.ratio)),
                           "Unit": str(self.unit),
                           "c_number": str(self.c_number),
                           "Creation Date": str(self.created_at),
                           "Finished at": str(self.end_time),
                           "Started at": str(self.start_time),
                           "unique_id": str(self.unique_id)})

    @classmethod
    def create(cls, title, profile, unit, c_number, priority, description='', unique_id=None):
        '''
        Creates a task.
        '''
        assert unique_id != None
        assert type(c_number) is float
        ratio = unit.ratio
        # TO-DO: Force entry to contain previous information
        task = cls(title=title, description=description, profile=profile, unit=unit, c_number=c_number, priority=priority, unique_id=unique_id)
        return task

    def complete(self, total_time):
        '''
        Creates a task.
        '''
        self.completed = True
        # To-DO: update the unit
        if self.unit.num_used != -1:
            update_ratio(total_time)

#### Load all the extension models
for model in glob2.glob('Dashboard/Extensions/**/models.py', recursive=True):
    import_module(model.replace('/', '.')[:-3])
