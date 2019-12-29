import os
import time
import datetime

from django.views import View
from django.conf import settings
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from qr_code.qrcode.utils import WifiConfig, QRCodeOptions

from user.models import User, UserFriend, Document
from .forms import NameForm, DocumentForm
from applibs.file_upload import FileUpload


# Create your views here.
class HomeView(View):

	def get(self, request):
		data = {}
		data['page_title'] = 'login'
		template = 'registration/login.html'

		return render(request, template, data)


class DashboardView(LoginRequiredMixin, View):

	def get(self, request):
		data = {}
		data['page_title'] = 'dashboard'
		template = 'dashboard.html'

		return render(request, template, data)


class UserView(View):

	def get(self, request):
		data = {}
		data['page_title'] = 'new user'
		template = 'pages/new_user.html'

		return render(request, template, data)

	def post(self, request):
		# print(request.POST)
		# return HttpResponse('Debugging...')

		# create a form instance and populate it with data from the request:
		form = NameForm(request.POST)

		# check whether it's valid:
		if form.is_valid():

			try:
				email = request.POST.get('email')
				password = request.POST.get('password')
				first_name = request.POST.get('first_name')
				last_name = request.POST.get('last_name')
				names = request.POST.getlist('name[]')
				ages = request.POST.getlist('age[]')

				user = User.objects.create_user(email, password, first_name=first_name, last_name=last_name)
				for key, value in enumerate(names):
					user_friend = UserFriend.objects.save(user, names[key], ages[key])

				if request.FILES.get('profile_img'):
					file = request.FILES.get('profile_img')
					uploaded_file_url = FileUpload.upload('users', file)
					# print(uploaded_file_url)
					document = Document.objects.save(user, uploaded_file_url)

			except Exception as e:
				raise e

			return redirect('view_user')

		return redirect('new_user')


class ViewUser(View):

	def get(self, request):
		data = {}
		data['page_title'] = 'users'
		data['users'] = User.objects.all_user()
		# data['qr_code_message'] = 'Hello World! I am Rakib.'
		# Use a WifiConfig instance to encapsulate the configuration of the connexion. 
		data['wifi_config'] = WifiConfig(
								ssid='my-wifi', 
								authentication=WifiConfig.AUTHENTICATION.WPA, 
								# password='P@$$w0rd',
								password='r01673120069',
							)
		data['qr_code_options'] = QRCodeOptions(size='10', border=6, error_correction='L')
		template = 'pages/user_list.html'

		# response = serializers.serialize('json', data['users'])
		# # response = serializers.serialize('json', data['users'], fields=('first_name','last_name','email'))
		# return HttpResponse(response)

		return render(request, template, data)


class UserEdit(View):
	
	def get(self, request, id):
		data = {}
		data['page_title'] = 'edit user'
		data['user'] = User.objects.get_user(id)
		template = 'pages/edit_user.html'

		return render(request, template, data)

	def post(self, request, id):
		# create a form instance and populate it with data from the request
		form = NameForm(request.POST)

		# check whether it's valid
		if form.is_valid():

			try:
				names = request.POST.getlist('name[]')
				ages = request.POST.getlist('age[]')

				user = User.objects.update_user(id, request.POST)
				# delete user friends
				UserFriend.objects.delete(user_id=id)
				for key, value in enumerate(names):
					user_friend = UserFriend.objects.save(user, names[key], ages[key])

				if request.FILES.get('profile_img'):

					old_file = Document.objects.get_document(user_id=id)

					if old_file:
						delete_file = settings.BASE_DIR+old_file.document
						if os.path.isfile(delete_file):
							os.remove(delete_file)
						Document.objects.delete(id=old_file.id)

					file = request.FILES.get('profile_img')
					uploaded_file_url = FileUpload.upload('users', file)
					# print(uploaded_file_url)
					document = Document.objects.save(user, uploaded_file_url)

			except Exception as e:
				raise e

			return redirect('view_user')

		return redirect('new_user')


class UserDelete(View):

	def get(self, request, id):

		try:
			old_file = Document.objects.get_document(user_id=id)
			User.objects.delete_user(id)

			if old_file:
				delete_file = settings.BASE_DIR+old_file.document
				if os.path.isfile(delete_file):
					os.remove(delete_file)

			return True
		except Exception as e:
			raise e
