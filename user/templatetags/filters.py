import os
import time
import datetime

from django import template
from django.conf import settings
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect
from user.models import User

register = template.Library()

@register.filter(name='get_user_type')
def get_user_type(id):

	staff_type = User.objects.get(id=id, is_active=True).is_staff
	
	if staff_type == 1:
		return 'Yes'
	else:
		return 'No'
