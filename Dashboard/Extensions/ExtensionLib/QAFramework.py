'''
Defines the question answer framework.
'''
import re
from django.forms import Form
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import logging
import traceback
from uuid import uuid4
from django.template import RequestContext
import timeout_decorator
import pdb
from django.shortcuts import render

#### Parameters
wait_time = 100; # Number of seconds to wait for a response for a question.
check_every = 5; # Number of seconds in between to check for fulfillment.

#### Global Variables


def ask(content, _type, previous_request, request=None, size="medium", checker=None):
	''' 
	Returns an HTMLResponse
	'''
	_type = _type.lower()
	if _type == "url":
		# Content is a url
		return JsonResponse({"redirect": content})
	elif _type == "url_newtab":
		# Content is a url
		return JsonResponse({"newtab": content})
	elif _type == "response":
		# Content is already HttpResponse
		return response
	elif _type == "html":
		# Content is a form
		return HttpResponse(content)
	elif _type == "form":
		# Assume it is html string
		return render(previous_request, 'ExtensionLib/FormFormat.html', context={'form': content})
	elif _type == "file":
		return render(content, request=request)
	else:
		logging.error("Unknown content type")
		raise("Unknown content type")
		traceback.print_exc()

