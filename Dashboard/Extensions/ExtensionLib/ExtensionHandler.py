from Dashboard.models import *
from django.http import HttpResponse, JsonResponse
import timeout_decorator
import types
import logging
import traceback
import pdb
from querystring_parser import parser
from django.shortcuts import render
import urllib

class ExtensionHandler:
	def __init__(self):
		self.request_dict = {}

	@staticmethod
	def close_response():
		'''
		Tells the client to close the modal view.
		'''
		return JsonResponse({"close_modal": True})

	@staticmethod
	def ackowledgement_response():
		'''
		Acknowledges information recieved.
		Usually a dummy response.
		'''
		return HttpResponse("acknowledged")

	def request_gotten(self, request):
		'''
		Keeps track of all users process through an extension modal.
		Users methods are stored in request_dict.

		'''
		p_data = request.POST
		user = request.user
		gen = None
		if "modal_closed" in p_data["data"].keys():
			print("Modal closed")
			# Delete instance of user's extension.
			# To-Do: Add timeout feature too.
			if p_data["modal_closed"] == True:
				del self.request_dict[user.id]
			return self.ackowledgement_response()
		elif "extension_selected" in p_data["data"].keys():
			print("UUID selected")
			# Load extension from database
			model = Extension.objects.filter(uuid=p_data["data"]["uuid"])
			assert len(model) == 1, "0 or multiple extensions by uuid found with uuid:" + str(uuid)
			model = model[0]
			extension = import_module(model.file_name)
			gen = getattr(extension, 'main')()
			assert isinstance(gen, types.GeneratorType), "Returned type isn't generator"
			self.request_dict[user.id] = gen
		elif "response" in p_data["data"].keys():
			# Continue extension from local dictionary
			gen = self.request_dict[user.id]
			request.response_data = parser.parse(request.POST["data"]["response"])
		elif "settings" in p_data["data"].keys():
			if 'uuid' not in p_data["data"].keys():
				return JsonResponse({'message':'Incomplete Post Data','explanation':'Include uuid in post request if settings is specified'}, status=400)
			model = Extension.objects.get(uuid=p_data["data"]['uuid'])
			form = None
			if model.sidebar_name != '':
				form = import_module(model.sidebar_name).SideBar
				form = form(user=user)
			return render(request, 'ExtensionLib/SideBarExtensionTemplate.html', context={'form': form, 'title': model.extension_name, 'uuid': p_data['data']['uuid']})
		elif 'extension_settings_save' in p_data['data'].keys():
			model = Extension.objects.get(uuid=p_data["data"]['uuid'])
			form = import_module(model.sidebar_name).SideBar
			data = urllib.parse.parse_qs(request.POST['data']['extension_settings_save'])
			form.save(request, data)
			return ExtensionHandler.ackowledgement_response()
		else:
			logger.error("Incomplete Post data" + str(p_data))
		# Try to get response out of generator. Send it
		# the request if it asks for it.
		try:
			response = gen.__next__()
			while response == None:
				response = gen.send(request)
			return response
		except StopIteration:
			return self.close_response()
		except Exception as e:
			logging.error("Failure in extension:"+str(e))
			traceback.format_exc()
