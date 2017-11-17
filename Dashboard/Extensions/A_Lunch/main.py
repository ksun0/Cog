'''
Gets today's lunch schedule.
'''
from Dashboard.Extensions.ExtensionLib.QAFramework import *
from .forms import *
import pdb
from bs4 import BeautifulSoup
import requests
from Dashboard.models import Event, Task
from datetime import datetime
extension_id = '93d50f7d-6da8-49e6-a38e-93f7cb3fb7db' # Used to identify this extension's events
MAX_DESCRIPTION_LENGTH = Event._meta.get_field('description').max_length

def create_breakfast_lunch_and_dinner(user):
	today = datetime.today().weekday()
	now = datetime.now()
	b_start_time = None
	b_end_time = None
	l_start_time = None
	l_end_time = None
	l_title = "Commons Lunch"
	if today < 5: # weekday
		b_start_time = now.replace(hour=7, minute=0)
		b_end_time = now.replace(hour=9, minute=15)
		l_start_time = now.replace(hour=11, minute=0)
		l_end_time = now.replace(hour=2, minute=0)
	else:
		b_start_time = now.replace(hour=10, minute=0)
		b_end_time = now.replace(hour=10, minute=30)
		l_start_time = now.replace(hour=10, minute=30)
		l_end_time = now.replace(hour=1, minute=30)
		l_title = 'Continental Breakfast'

	Event.objects.filter(extension_id=extension_id).delete()
	breakfast = Event.objects.create(title="Andover Breakfast",
										description='',
										profile=user.profile,
										start_time=b_start_time,
										end_time=b_end_time,
										extension_id=extension_id)
	lunch = Event.objects.create(title=l_title,
										description='',
										profile=user.profile,
										start_time=b_start_time,
										end_time=b_end_time,
										extension_id=extension_id)
	dinner = Event.objects.create(title="Commons Dinner",
										description='',
										profile=user.profile,
										start_time=now.replace(hour=5, minute=0),
										end_time=now.replace(hour=7, minute=0),
										extension_id=extension_id)
	lunch.save()
	return breakfast, lunch, dinner

def get_meal_summary(meal_id):
	url = 'http://phillipsacademy.campusdish.com/Commerce/Catalog/Menus.aspx?LocationId=4236&PeriodId='+str(meal_id)+'&MenuDate=&Mode=day&UIBuildDateFrom='
	soup = BeautifulSoup(requests.get(url).content)
	items = soup.findAll('a', {'rel':'prettyPhotoiFrameWithoutNavigation'}, text=True)
	for i in range(len(items)):
		items[i] = items[i].getText()
	summary = ', '.join(items)
	if len(summary) > MAX_DESCRIPTION_LENGTH:
		summary = summary[:MAX_DESCRIPTION_LENGTH-1] + '…'
	return summary


def main():
	request = yield
	b, l, d = create_breakfast_lunch_and_dinner(request.user)
	b.description = get_meal_summary(2054)
	l.description = get_meal_summary(2056)
	d.description = get_meal_summary(2057)
	l.save()
	b.save()
	d.save()
