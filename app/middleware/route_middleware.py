from django.urls import resolve
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class RouteAccess(MiddlewareMixin):

	def process_request(self, request):

		urls = ['dashboard', 'view_user', 'new_user', 'edit_user']
		# get current url name
		current_url = resolve(request.path_info).url_name

		if current_url in urls:
			if not request.user.is_authenticated:
				return redirect('home')
