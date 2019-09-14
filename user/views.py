from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View

from .forms import NameForm
from user.models import User

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
			email = request.POST['email']
			password = request.POST['password']
			first_name = request.POST['first_name']
			last_name = request.POST['last_name']

			user = User.objects.create_user(email, password, first_name=first_name, last_name=last_name)

			return redirect('view_user')

		return redirect('new_user')


class ViewUser(View):

	def get(self, request):
		data = {}
		data['page_title'] = 'users'
		template = 'pages/user_list.html'

		return render(request, template, data)
