import web
import urlparse
import json

import auctionDb

class Login:
	def POST(self):
		session = web.config._session
		data = urlparse.parse_qs(web.data())
		print 'POST MADE to /ajax/login'
		username = data['username'][0]
		password = data['password'][0]
		userid = auctionDb.login(username, password)
		result = {}
		if userid != -1:
			session.loggedin = True
			session.username = username
			session.userid = userid
			result['success'] = True
		else:
			session.loggedin = False
			result['success'] = False
		return json.dumps(result)

class Reset:
	def GET(self):
		session = web.config._session
		session.kill()
		return 'the wolf dead'

class Register:
	def POST(self):
		data = urlparse.parse_qs(web.data())
		print 'POST MADE to /ajax/register'
		username = data['username'][0]
		password = data['password'][0]
		email = data['email'][0]
		result = {}
		if email in ['javi.muhrer@gmail.com']:
			auctionDb.register(username, password, email)
			result['success'] = True
		else:
			result['success'] = False
		return json.dumps(result)