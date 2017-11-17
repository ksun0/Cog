from Dashboard.Extensions.ExtensionLib.SideBar import SideBar
from django import forms
from .models import *
import pdb

class SideBar(forms.Form):
	your_name = forms.CharField(label='Your name', max_length=100)
	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user')
		users = TestModel.objects.filter(user=user.profile)
		super(SideBar, self).__init__(*args, **kwargs)
		if len(users) == 1:
			self.fields['your_name'].widget.attrs['placeholder'] = users[0].name

	def save(request, data):
		name = data['your_name'][0]
		users = TestModel.objects.filter(user=request.user.profile)
		if len(users) == 0:
			TestModel.objects.create(user=request.user.profile, name=name)
		elif len(users) == 1:
			users[0].name = name
			users[0].save()
