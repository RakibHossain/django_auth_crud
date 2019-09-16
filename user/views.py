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
		data['users'] = User.objects.all_user()
		template = 'pages/user_list.html'

		# return HttpResponse(data['users'])
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
			return redirect('view_user')
		return redirect('new_user')


class UserDelete(View):

	def get(self, request, id):
		user = get_object_or_404(User, pk=pk)
		user.delete()
		return redirect('user_list')	
