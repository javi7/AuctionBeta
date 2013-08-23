import web

import auctionDb

class TempletorUtils:
	session = None
	template = web.template
	weeks = auctionDb.getAllWeeks()
	filters = None
	users = auctionDb.getAllTeamNames()

	def __init__(self, session=None, filters=None):
		self.session = session
		self.filters = filters

def getTemplateSystem(session=None, filters=None):
	return web.template.render('html/pages', globals = {
		'utils': TempletorUtils(session, filters)
	})

class Rules:
	def GET(self):
		session = web.config._session
		return str(getTemplateSystem(session).rules())

class Home:
	def GET(self):
		session = web.config._session
		if 'userid' in session and session.userid != None:
			return str(getTemplateSystem(session).home())
		else:
			return str(getTemplateSystem(session).register())


class Bid:
	def GET(self):
		session = web.config._session
		userId = session.userid
		filters = web.input(pos='All', offset=0, search="", week=None, avail='Available', showBids='Hide')
		if filters.week != None:
			filters.week = int(filters.week)
		else:
			filters.week = auctionDb.getCurrentWeek()
		playerList = auctionDb.getNflPlayersForBidding(userId, filters.pos, filters.offset, 
			filters.week, filters.search, filters.avail, filters.showBids)
		return str(getTemplateSystem(session, filters).bid(playerList))

class Team:
	def GET(self):
		session = web.config._session
		userId = session.userid
		filters = web.input(week=None, team=None)
		if filters.team == None:
			filters.team = auctionDb.getUser(userId=userId)['user_alias']
		else:
			userId = auctionDb.getUser(username=filters.team)['user_id']
		if filters.week != None:
			filters.week = int(filters.week)
		else:
			filters.week = auctionDb.getCurrentWeek()
		rosterList = auctionDb.getLineup(userId, filters.week)
		bidList = auctionDb.getUserBids(userId, filters.week)
		filters.userId = userId
		return str(getTemplateSystem(session, filters).team(rosterList, bidList))
