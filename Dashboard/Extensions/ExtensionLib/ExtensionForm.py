from django import forms
from querystring_parser import parser

class ExtensionForm(forms.Form):
	pass
	# @staticmethod
	# def parse(request):
	# 	super().__init__(parser.parse(request.POST["data"]["response"]).data)
