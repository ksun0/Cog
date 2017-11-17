from django import forms
class SideBar(forms.Form):
	def __init__(self, *args, **kwargs):
		if 'user' in kwargs:
			kwargs.pop('user')
		super(SideBar, self).__init__(*args, **kwargs)

	def save():
		print("Please define a save feature if you'd like your module to save settings.")