from Dashboard.Extensions.ExtensionLib.ExtensionForm import ExtensionForm
from django import forms
from .models import TestModel

class TestForm(ExtensionForm):
	your_name = forms.CharField(label='Your name', max_length=100)
	choices = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=[1,2,3,4])
