from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View

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
