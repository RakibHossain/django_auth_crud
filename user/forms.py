from django import forms

class NameForm(forms.Form):
	email = forms.EmailField(label='Your email', max_length=100)
	