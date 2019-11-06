from django.urls import resolve
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class RouteAccess(MiddlewareMixin):

	def process_request(self, request):

		# get current url name
		current_url = resolve(request.path_info).url_name
		if not current_url == 'view_user':
			return HttpResponse("Sorry, you are not allowed to access this route.")
