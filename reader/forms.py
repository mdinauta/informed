from django import forms
from django.forms import ModelForm, CharField
from django.forms.formsets import formset_factory

from .models import feed

class feed_form(ModelForm):
	class Meta:
		model = feed
		exclude = ['user']