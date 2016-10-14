#!/usr/bin/env python

from cgi import parse_qs
import signapp

def application(environ, start_response):
	## passing environ uwsgi PARAM
	try:
		request_body_size = int(environ.get('CONTENT_LENGTH', 0))
	except (ValueError):
		request_body_size = 0
	uri = environ['REQUEST_URI']
	request_body = environ['wsgi.input'].read(request_body_size)
	post = parse_qs(request_body)
	## Declare apps
	sign = signapp.Signapp()
	## Menu Logic
	url=sign.urlDecode16(uri[:1])
	if sign.getMenu(url[:3])=="key":
		data = url[4:]
		result = ''
		for a in sign.getAllSign(data):
			result=result+str(a)
		hbegin = sign.getHtmlBegin()
		hend = sign.getHtmlEnd()
		respon = hbegin + result + hend
	if sign.getMenu(url[:3])=="token":
		token = post.get('token', [''])[0]
		html = sign.getTokenData(token)
		email = sign.getJsonData('email',html)
		respon = email
	else:
		result = "ganteng"
		hbegin = sign.getHtmlBegin()
		hend = sign.getHtmlEnd()
		hend = hend.replace("TOKENURIPARAM",sign.tokenUri(),1)
		respon = hbegin + result + hend
	## Passing HTML to client
	start_response('200 OK', [('Content-Type', 'text/html'),('Content-Length', str(len(respon)))])
	return [respon]

