from django.http import HttpResponse, JsonResponse
from models import *

def step_1():
	return HttpResponse("Andover Schedule Test")

steps = [step_1]
name = "Andover Schedule"
description = "This extension will load your course schedules from the website."