import os
import time
import datetime

from django.views import View
from django.conf import settings
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.mixins import LoginRequiredMixin
from qr_code.qrcode.utils import WifiConfig, QRCodeOptions

from user.models import User, Document
from .forms import NameForm, DocumentForm


class FileUpload():

	def upload(path, file):
		file_path = path+'/'+datetime.date.today().isoformat()
		fs = FileSystemStorage(location='media/'+file_path)
		tempname = str(time.time_ns())+'.png'
		filename = fs.save(tempname, file)
		file_original_path = file_path+'/'+str(filename)
		uploaded_file_url = fs.url(file_original_path)

		return uploaded_file_url


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
		# create a form instance and populate it with data from the request:
		form = NameForm(request.POST)

		# check whether it's valid:
		if form.is_valid():
			email = request.POST.get('email')
			password = request.POST.get('password')
			first_name = request.POST.get('first_name')
			last_name = request.POST.get('last_name')

			if request.FILES.get('profile_img'):
				file = request.FILES.get('profile_img')
				uploaded_file_url = FileUpload.upload('users', file)
				# print(uploaded_file_url)

			user = User.objects.create_user(email, password, first_name=first_name, last_name=last_name)
			document = Document.objects.save(user, uploaded_file_url)
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
			user = User.objects.update_user(id, request.POST)
			old_file = Document.objects.get_document(user_id=id)

			try:
				delete_file = settings.BASE_DIR+old_file.document

				if request.FILES.get('profile_img'):
					if os.path.isfile(delete_file):
						os.remove(delete_file)

					file = request.FILES.get('profile_img')
					uploaded_file_url = FileUpload.upload('users', file)
					# print(uploaded_file_url)

					Document.objects.delete(id=old_file.id)
					document = Document.objects.save(user, uploaded_file_url)
			except Exception as e:
				raise e

			return redirect('view_user')

		return redirect('new_user')


class UserDelete(View):

	def get(self, request, id):

		try:
			old_file = Document.objects.get_document(user_id=id)
			delete_file = settings.BASE_DIR+old_file.document
			User.objects.delete_user(id)

			if os.path.isfile(delete_file):
				os.remove(delete_file)

			return True
		except Exception as e:
			raise e
