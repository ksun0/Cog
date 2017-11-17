from django.utils import timezone
from django.utils.dateparse import parse_datetime
from .forms import LoginForm
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.contrib.auth.views import login as loginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from Cog import settings
from .models import *
from .forms import SignupForm
import urllib
import json
from Dashboard.utils import *
from django.contrib.auth.decorators import login_required
import httplib2
from pprint import pprint
import logging
import pdb
from importlib import import_module
import simplejson
import traceback
from Dashboard.Extensions.ExtensionLib.ExtensionHandler import ExtensionHandler

extension_handler = ExtensionHandler()

# Create your views here.
def Landing(request):
	user = request.user
	if user is not None and user.is_active:
		return HttpResponseRedirect(request.GET.get('next', '/dashboard'))
	return render(request, 'Dashboard/landing.html')

def Dashboard(request):

	def stringToDate(string):
		# assumes format "08/05/2017 10:30 PM" from datetime picker
		date, time, am_pm = string.split(" ")
		month, day, year = date.split("/")
		hour, minute = time.split(":")
		hour = int(hour)%12
		if am_pm == "PM":
			hour = hour + 12
		tz = timezone.get_default_timezone() # America/New_York
		# TODO: get user's own timezone
		out = datetime.datetime(int(year), int(month), int(day), hour, int(minute))#, tzinfo=tz)
		return out
	# Get user and test if logged in.
	user = request.user
	if user is None or not user.is_active:
		return HttpResponseRedirect(request.GET.get('next', '/login'))
	# Get tasks and events
	prof = user.profile;
	events = prof.event_set.get_queryset();
	tasks = prof.task_set.get_queryset();
	tasks = json.dumps([str(x) for x in tasks])
	events = json.dumps([str(x) for x in events])

	#Post data
	if request.method == "POST":
		logging.info(request.POST.keys())
		# print(request.POST["uuid"])
		logging.info(request.POST["action"])
	if request.method == "POST" and "action" in request.POST.keys():
		def delete_task(uuid):
			logging.info("Deleting task", uuid)
			tasks = Task.objects.filter(unique_id=uuid)
			if len(tasks) > 0:
				for deleted_task in tasks:
					# Just in case there are multiple. There shouldn't be.
					deleted_priority = deleted_task.priority
					deleted_task.delete()
					lower_tasks = Task.objects.filter(priority__gt=deleted_priority)
					for task in lower_tasks:
						task.priority = task.priority - 1
						task.save()
			else:
				logging.error("Requesting to delete non-existant task.")
			if len(tasks) > 1:
				logging.error("Multiple tasks with same uuid in deleting action")
		if request.POST["action"] == "add_custom_unit":
			# Adding unit
			if len(Unit.objects.filter(title=request.POST["title"])) == 0: # prevent duplicate units by title
				title = request.POST.get('title')
				description = request.POST.get('description')
				c_num = float(request.POST.get('c_number'))*60
				u = Unit(title=title, description=description, profile_id=prof.id, ratio=c_num)
				u.save()
		elif request.POST["action"] == "delete_custom_unit":
			u = Unit.objects.get(title=request.POST["title"])
			tasks_to_delete = Task.objects.filter(unit=u)
			for t in tasks_to_delete:
				delete_task(t.unique_id)
			u.delete()
		elif request.POST["action"] == "delete":
			if request.POST.get('toggle') == 'task':
				delete_task(request.POST["uuid"])
			else:
				print("Deleting event", request.POST["uuid"])
				Event.objects.filter(unique_id=request.POST["uuid"]).delete()
		elif request.POST["action"] == 'delete_task':
			# there are two forms by which tasks can be deleted; one from the
			# modal and the other from the task table view
			delete_task(request.POST["uuid"])
		elif request.POST['action'] == 'delete_event':
			Event.objects.filter(unique_id=request.POST["uuid"]).delete()
		elif request.POST["action"] == "add_job":
			#Adding or task
			user = request.user
			profile = user.profile
			title = request.POST['title']
			description = request.POST['description']
			uuid = request.POST["uuid"]
			existing_task = Task.objects.all().filter(unique_id=uuid)
			existing_task = existing_task[0] if len(existing_task) > 0 else None
			if request.POST.get('toggle') == 'task':
				unit_string = request.POST.get('unit')
				unit = Unit.objects.get(profile_id__in=[profile.id, 0], title=unit_string)
				c_number = request.POST.get('c_number')
				c_number = float(c_number)

				if existing_task == None:
					next_priority = Task.objects.filter(priority__gt=0).count() + 1
					t = Task.create(title, profile, unit, c_number, next_priority, description=description, unique_id=uuid)
					t.save()
				else:
					existing_task.title = title
					existing_task.profile = profile
					existing_task.unit = unit
					existing_task.c_number = c_number
					existing_task.description = description
					existing_task.uuid = uuid
					existing_task.save()
			else: #for the events
				start_time_string = request.POST.get('start')
				end_time_string = request.POST.get('end')
				start_time = stringToDate(start_time_string)
				end_time = stringToDate(end_time_string)
				e = Event(title=title, description=description, profile=profile, start_time=start_time, end_time=end_time)
				e.save()
		elif request.POST["action"] == 'raise_task_priority':
			lesser_task = Task.objects.get(unique_id=request.POST['uuid'])
			lesser_priority = lesser_task.priority
			greater_task = Task.objects.get(priority=lesser_priority-1)
			lesser_task.priority = lesser_priority-1
			greater_task.priority = lesser_priority
			lesser_task.save()
			greater_task.save()
		elif request.POST["action"] == 'lower_task_priority':
			greater_task = Task.objects.get(unique_id=request.POST['uuid'])
			greater_priority = greater_task.priority
			print(greater_task.title, greater_priority)
			lesser_task = Task.objects.get(priority=greater_priority+1)
			greater_task.priority = greater_priority+1
			lesser_task.priority = greater_priority
			lesser_task.save()
			greater_task.save()
		return HttpResponseRedirect('/dashboard/')
	return render(request, 'Dashboard/base.html', {'tasks': str(tasks), 'events': str(events)})

def Login(request):
    next = request.GET.get('next', '/dashboard')
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if request.POST and login_form.is_valid():
            user = login_form.login(request)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    print(user, "logged in")
                    return HttpResponseRedirect(next)
                else:
                    return HttpResponse("Inactive user.")
        else:
            return render(request, "Dashboard/login.html", {'redirect_to': next, "login_form": login_form})
    return render(request, "Dashboard/login.html", {'redirect_to': next})

def Logout(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)

def Signup(request):
	next = request.GET.get('next', '/dashboard')
	if request.method == 'POST':
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		form = SignupForm(request.POST)
		if form.is_valid():
			new_user = User.objects.create_user(username=username, email=email, password=password)
			new_profile = Profile(user=new_user)
			new_profile.save()
			# u = Unit(title="default", description="default", profile_id=new_profile.id)
			# u.save()
			login(request, new_user)
			return HttpResponseRedirect(next)
		else:
			return render(request, "Dashboard/signup.html", {'redirect_to': next, 'form': form})
	return render(request, "Dashboard/signup.html", {'redirect_to': next})

def getTasks(request):
	user = request.user;
	if request.method == "GET" and user.is_active:
		taskList = []
		for task in user.profile.task_set.all():
			taskList.append(str(task))
		return JsonResponse(taskList, safe=False)
	return HttpResponseRedirect(request.GET.get('next', '/login'))

def getEvents(request):
	user = request.user;
	if request.method == "GET" and user.is_active:
		eventList = []
		for event in user.profile.event_set.all():
			eventList.append(str(event))
		return JsonResponse(eventList, safe=False)
	return HttpResponseRedirect(request.GET.get('next', '/login'))

def getAllUnits(request):
	user = request.user;
	if request.method == "GET" and user.is_active:
		retList = []
		for unit in Unit.objects.filter(profile_id__in=[user.profile.id, 0]):
			unitDict = {}
			unitDict['title'] = str(unit.title)
			unitDict['description'] = str(unit.description)
			unitDict['ratio'] = str(unit.ratio)
			retList.append(unitDict)
		return JsonResponse(retList, safe=False)
	return HttpResponseRedirect(request.GET.get('next', '/login'))

def getCustomUnits(request):
	user = request.user;
	if request.method == "GET" and user.is_active:
		retList = []
		for unit in Unit.objects.filter(profile_id=user.profile.id):
			unitDict = {}
			unitDict['title'] = str(unit.title)
			unitDict['description'] = str(unit.description)
			unitDict['ratio'] = str(unit.ratio)
			retList.append(unitDict)
		return JsonResponse(retList, safe=False)
	return HttpResponseRedirect(request.GET.get('next', '/login'))

def Settings(request):
	return render(request, 'Dashboard/settings.html')

def getJobs(request):
	user = request.user;
	if request.method == "GET" and user.is_active:
		eventList = []
		for event in user.profile.event_set.all():
			eventList.append(str(event))
		taskList = []
		for task in user.profile.task_set.all():
			taskList.append(str(task))
		return JsonResponse([taskList, eventList], safe=False)
	return HttpResponseRedirect(request.GET.get('next', '/login'))

def extensions(request):
	# Check if user is logged in
	user = request.user
	if user is None or not user.is_active:
		return HttpResponseRedirect(request.GET.get('next', '/login'))
	# Check if just listing
	if "list" in request.GET.keys():
		return JsonResponse([(x.json_encode(), x.sidebar_name != '') for x in Extension.objects.all()], safe=False)
	try:
		# Get function for correct step
		request.POST = dict(request.POST)
		if 'data' in request.POST.keys():
			request.POST["data"] = json.loads(request.POST["data"][0])
		else:
			logging.info('Incomplete post data')
			return JsonResponse({'message':'Incomplete Post Data','explanation':'Include data in post request'}, status=400)
		response = extension_handler.request_gotten(request)
		assert isinstance(response, HttpResponse), "Extension's view didn't return a response. It returned a"+str(type(response))
	except Exception as e:
		logging.error('Extensions failed with error: '+str(e))
		traceback.print_exc()
		return HttpResponse(status=500)
	return response

