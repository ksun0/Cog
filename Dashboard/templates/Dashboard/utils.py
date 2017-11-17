def parseTime(timeStr):
	# Parse Times
	if timeStr == '':
		return None
	if ":" in total_time_string:
		h = int(re.search('[0-9]+(?=:)', total_time_string).group())
		m = int(re.search('(?<=:)[0-5][0-9]', total_time_string).group())
	else:
		t = int(total_time_string)
		h = t//60
		m = t%60
	total_time = timezone.timedelta(hours=h, minutes=m)
	return total_time