import web
import urlparse
import json

import auctionDb

class Bid:
	def POST(self):
		session = web.config._session
		data = urlparse.parse_qs(web.data())
		print "POST MADE TO /api/bid -- " + str(data)
		result = {}
		if 'userid' in session:
			auctionDb.placeBid(session.userid, data['playerId'][0], data['bidAmount'][0], data['weekId'][0])
			result['success'] = True
		else:
			result['success'] = False
		return json.dumps(result)

	def DELETE(self):
		session = web.config._session
		data = urlparse.parse_qs(web.data())
		print "\DELETE MADE TO /api/bid -- " + str(data)
		result = {}
		if 'userid' in session:
			auctionDb.cancelBid(session.userid, data['playerId'][0], data['weekId'][0])
			result['success'] = True
		else:
			result['success'] = False
		return json.dumps(result)

class Keep:
	def POST(self):
		session = web.config._session
		data = urlparse.parse_qs(web.data())
		print "POST MADE TO /api/keep -- " + str(data)
		result = {}
		if 'userid' in session:
			numKeepers = auctionDb.getNumKeepers(session.userid, data['weekId'][0])
			if numKeepers < 2 or data['keep'][0] == '0':
				auctionDb.changePlayerKeepStatus(session.userid, data['playerId'][0], data['weekId'][0], data['keep'][0])
				result['success'] = True
			else:
				result['success'] = False
				result['failure'] = 'HOARDER! You may only keep two players.'
		else:
			result['success'] = False
			result['failure'] = 'Please log in to perform this task, son.'
		return json.dumps(result)