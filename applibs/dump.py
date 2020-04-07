from django.core import serializers


def dd(request, data=''):
	scheme      = request.scheme
	server_name = request.META['SERVER_NAME']
	server_port = request.META['SERVER_PORT']
	remote_addr = request.META['REMOTE_ADDR']
	user_agent  = request.META['HTTP_USER_AGENT']
	path        = request.path
	method      = request.method
	session     = request.session
	cookies     = request.COOKIES

	get_data = {}
	for key, value in request.GET.lists():
		get_data[key] = value

	post_data = {}
	for key, value in request.POST.lists():
		post_data[key] = value

	files = {}
	for key, value in request.FILES.lists():
		files['name'] = request.FILES[key].name
		files['content_type'] = request.FILES[key].content_type
		files['size'] = request.FILES[key].size

	query_data     = ''
	executed_query = ''
	if data:
		executed_query = data.query
		query_data = serializers.serialize('json', data)

	msg = f'''
		<html>
			<span style="color: red;"><b>Scheme</b></span>        : <span style="color: blue;">{scheme}</span><br>
			<span style="color: red;"><b>Server Name</b></span>   : <span style="color: blue;">{server_name}</span><br>
			<span style="color: red;"><b>Server Port</b></span>   : <span style="color: blue;">{server_port}</span><br>
			<span style="color: red;"><b>Remote Address</b></span>: <span style="color: blue;">{remote_addr}</span><br>
			<span style="color: red;"><b>User Agent</b></span>    : <span style="color: blue;">{user_agent}</span><br>
			<span style="color: red;"><b>Path</b></span>          : <span style="color: blue;">{path}</span><br>
			<span style="color: red;"><b>Method</b></span>        : <span style="color: blue;">{method}</span><br>
			<span style="color: red;"><b>Session</b></span>       : <span style="color: blue;">{session}</span><br>
			<span style="color: red;"><b>Cookies</b></span>       : <span style="color: blue;">{cookies}</span><br>
			<span style="color: red;"><b>Get Data</b></span>      : <span style="color: blue;">{get_data}</span><br>
			<span style="color: red;"><b>Post Data</b></span>     : <span style="color: blue;">{post_data}</span><br>
			<span style="color: red;"><b>Files</b></span>         : <span style="color: blue;">{files}</span><br>
			<span style="color: red;"><b>Executed Query</b></span>: <span style="color: blue;"><br>{executed_query}</span><br>
			<span style="color: red;"><b>Query Data</b></span>    : <span style="color: blue;"><br>{query_data}</span><br>
		</html>
	'''

	return msg
