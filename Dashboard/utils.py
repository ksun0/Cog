from django.utils import timezone
import re
def parse_time(timeStr):
	# Parse Times
	if timeStr == '':
		return None
	if ":" in timeStr:
		h = int(re.search('[0-9]+(?=:)', timeStr).group())
		m = int(re.search('(?<=:)[0-5][0-9]', timeStr).group())
	else:
		t = int(timeStr)
		h = t//60
		m = t%60
	total_time = timezone.timedelta(hours=h, minutes=m)
	return total_time


def set_cookie(response, key, value, days_expire = 7):
	if days_expire is None:
		max_age = 365 * 24 * 60 * 60  #one year
	else:
		max_age = days_expire * 24 * 60 * 60 
	expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
	response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN, secure=settings.SESSION_COOKIE_SECURE or None)