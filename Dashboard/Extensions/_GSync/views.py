from oauth2client.contrib import xsrfutil # To-Do: update to google-auth. Oauth2client is deprecated. See https://google-auth.readthedocs.io/en/latest/oauth2client-deprecation.html
from oauth2client.client import flow_from_clientsecrets, OAuth2WebServerFlow
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from Cog import settings
import httplib2
from googleapiclient.discovery import build
from .models import *
from django.shortcuts import render, redirect
import os
from django.template.loader import render_to_string
from forms import *
import pdb


DEPLOYMENT_URL = settings.FULL_HOST
# Change DEPLOYMENT_URL to "https://www.cogtest-3376185029.ddns.net:8820" if locally deploying
FLOW = flow_from_clientsecrets(
    settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
    scope='https://www.googleapis.com/auth/calendar',
    redirect_uri=DEPLOYMENT_URL+'/api/extensions/',
    prompt='consent')

def authorize(data, rerun=False):
	print('authorize')
	request = data["request"]
	storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
	credential = storage.get()
	if rerun or credential is None or credential.invalid == True:
		FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY, request.user)
		authorize_url = FLOW.step1_get_authorize_url()
		return (1, JsonResponse({'redirect': authorize_url}))
	google_auth_return(data, rerun) # Next step

def google_auth_return(data, rerun=False):
	'''
	Authenticates google calendars
	'''
	print("google_auth_return")
	pg_data = data["pg_data"]
	request = data["request"]
	if 'state' in pg_data and 'code' in pg_data:
		# Save credentials
		if rerun or not xsrfutil.validate_token(settings.SECRET_KEY, pg_data["state"].encode('UTF-8'),
		                             request.user):
			return  HttpResponseBadRequest()
		credential = FLOW.step2_exchange(pg_data)
		storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
		storage.put(credential)
	else:
		authorize(data, True)
	get_calendars(data)

def get_calendars(data):
	print('get_calendars')
	service = None
	request = data["request"]
	user = request.user
	profile = user.profile

	# Get user google credentials
	storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
	credential = storage.get()

	http = credential.authorize(httplib2.Http())
	service = build("calendar", "v3", http=http)
	cal_page_token = None
	
	try:
		cal_list = profile.calendarlist
	except:
		cal_list = CalendarList(profile=profile)
		cal_list.save()
		profile.calendarlist = cal_list
		profile.save()
	# To-DO: Sync all calendars.
	while True:
		gcal_list = service.calendarList().list(pageToken=cal_page_token).execute()
		for calendar_list_entry in gcal_list['items']:
			if len(Calendar.objects.filter(title=calendar_list_entry['summary'])) == 0:
				cal = Calendar(title=calendar_list_entry['summary'], cal_id=calendar_list_entry['id'], handler=cal_list)
				cal.save()

		cal_page_token = gcal_list.get('nextPageToken')
		if not cal_page_token:
			break
	calendar_form = CalendarSelectForm(calendars=[x.title for x in cal_list.calendar_set.all()])
	html_str =  render_to_string('GSync/templates/select_calendars.html', request=request, context={'form': calendar_form})
	return (3, HttpResponse(html_str))

def get_events(data):
	print('get_events')
	request = data["request"]
	storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
	credential = storage.get()

	http = credential.authorize(httplib2.Http())
	service = build("calendar", "v3", http=http)
	events = []
	page_token = None
	calendars = data["request"].GET.getlist("calendars")
	for calendar in calendars:
		while True:
			c_events = service.events().list(calendarId=calendar,pageToken=page_token).execute()
			# To-Do: add intelligent time range
			for event in c_events['items']:
				events.append(event)
			page_token = c_events.get('nextPageToken')
			if not page_token:
				break

	for event in events:
		# To-Do: Switch to bulk event upload
		try:
			start_time = event['start']['date'] if 'date' in event['start'].keys() else event['start']['dateTime']
			end_time = event['end']['date'] if 'date' in event['start'].keys() else event['end']['dateTime']
			start_time = parse_datetime(start_time)
			end_time = parse_datetime(end_time)
			if (Event.objects.filter(title=event["summary"], description="default", profile=profile, start_time=start_time, end_time=end_time).count() == 0):
				e = Event(title=event["summary"], description="default", profile=profile, start_time=start_time, end_time=end_time)
				e.save()
		except Exception as e:
			print("Error", e)
	print(events)
	return (None, None)

steps = [authorize, google_auth_return, get_calendars, get_events]
name = "Google Calendar Sync"
description = "Syncs your schedule to google calendar."