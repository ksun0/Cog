from django import forms

class CalendarSelectForm(forms.Form):
	def __init__(self, *args, **kwargs):
		calendars = kwargs.pop('calendars')
		super(CalendarSelectForm, self).__init__(*args, **kwargs)
		calendars = forms.MultipleChoiceField(
		        required=True,
		        widget=forms.CheckboxSelectMultiple,
		        choices=zip(calendars, calendars),
		    )
		# calendars.widget.attrs.update({'class' : 'list-group-item'})
		self.fields['calendars'] = calendars
		self.Meta.fields.append('calendars')

	class Meta:
		fields = []
		# widgets = {
  #           'myfield': forms.TextInput(attrs={'class': 'myfieldclass'}),
  #       }