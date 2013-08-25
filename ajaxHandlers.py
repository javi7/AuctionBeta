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
		user = auctionDb.login(username, password)
		result = {}
		if user != None:
			session.loggedin = True
			session.username = user['user_alias']
			session.userid = user['user_id']
			result['success'] = True
		else:
			session.loggedin = False
			result['success'] = False
		return json.dumps(result)

class Reset:
	def POST(self):
		session = web.config._session
		session.kill()
		result = {}
		result['success'] = True
		return json.dumps(result)

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

class ChangeAccount:
	def POST(self):
		session = web.config._session
		result = {}
		if 'userid' in session and session.userid != None:
			userId = session.userid
			data = urlparse.parse_qs(web.data())
			password = data['password'][0]
			changeValue = data['changeValue'][0]
			field = data['field'][0]
			if auctionDb.verifyPassword(userId, password):
				if field ==  'newpassword':
					auctionDb.changePassword(userId, changeValue)
					result['success'] = True
				elif field == 'teamname':
					auctionDb.changeTeamName(userId, changeValue)
					result['success'] = True
				elif field == 'email':
					auctionDb.changeEmail(userId, changeValue)
					result['success'] = True
				else:
					result['success'] = False
					result['failure'] = 'invalid field to change!'
			else:
				result['success'] = False
				result['failure'] = 'invalid password!'
		else:
			result['success'] = False
			result['failure'] = 'not logged in!'
		return json.dumps(result)