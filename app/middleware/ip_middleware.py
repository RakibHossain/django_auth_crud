from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class IPAccess(MiddlewareMixin):
	
	# Check if client IP is allowed
	def process_request(self, request):

		# Authorized ip's
		allowed_ips = ['192.168.0.102', '127.0.0.1']
		# Get client IP
		ip = request.META.get('REMOTE_ADDR')
		if ip not in allowed_ips:
			# If user is not allowed raise Error
			# raise Http403
			return HttpResponse("Sorry, you are not allowed.")

		# If IP is allowed we don't do anything
		return None
