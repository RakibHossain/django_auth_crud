from django import forms
from user.models import Document


class NameForm(forms.Form):
	email = forms.EmailField(label='Your email', max_length=100)


class DocumentForm(forms.ModelForm):
	class Meta:
		model = Document
		fields = ('document',)
	