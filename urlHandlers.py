import web

import auctionDb

class TempletorUtils:
	session = None
	template = web.template
	weeks = None
	filters = None
	users = None

	def __init__(self, session=None, filters=None):
		self.session = session
		self.filters = filters
		self.weeks = auctionDb.getAllWeeks()
		self.users = auctionDb.getAllTeamNames()

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

class Account:
	def GET(self):
		session = web.config._session
		if 'userid' in session and session.userid != None:
			return str(getTemplateSystem(session).account())
		else:
			return str(getTemplateSystem(session).accessDenied())

class Bid:
	def GET(self):
		session = web.config._session
		if 'userid' in session and session.userid != None:
			userId = session.userid
			filters = web.input(pos='All', offset=0, search="", week=None, avail='Available', showBids='Hide')
			if filters.week != None:
				filters.week = int(filters.week)
			else:
				filters.week = auctionDb.getCurrentWeek()
			playerList, filters.next = auctionDb.getNflPlayersForBidding(userId, filters.pos, int(filters.offset), 
				filters.week, filters.search, filters.avail, filters.showBids)
			filters.prev = filters.offset > 0
			return str(getTemplateSystem(session, filters).bid(playerList))
		else:
			return str(getTemplateSystem(session).accessDenied())

class Team:
	def GET(self):
		session = web.config._session
		filters = web.input(week=None, team=None)
		if filters.team != None:
			userId = auctionDb.getUser(username=filters.team)['user_id']
		elif 'userid' in session and session.userid != None:
			userId = session.userid
			filters.team = auctionDb.getUser(userId=userId)['user_alias']
		else:
			filters.team = auctionDb.getAllTeamNames()[0]
			userId = auctionDb.getUser(username=filters.team)['user_id']
		if filters.week != None:
			filters.week = int(filters.week)
		else:
			filters.week = auctionDb.getCurrentWeek()
		rosterList = auctionDb.getLineup(userId, filters.week)
		bidList = auctionDb.getUserBids(userId, filters.week)
		filters.userId = userId
		return str(getTemplateSystem(session, filters).team(rosterList, bidList))

class Standings:
	def GET(self):
		session = web.config._session
		standingsList = auctionDb.getStandingsList()
		return str(getTemplateSystem(session).standings(standingsList))

class Scoreboard:
	def GET(self):
		session = web.config._session
		filters = web.input(week=None)
		if filters.week == None:
			filters.week = auctionDb.getCurrentWeek()
		else:
			filters.week = int(filters.week)
		weekMatchups = auctionDb.getWeekMatchups(filters.week)
		matchupScores = auctionDb.getMatchupScores(filters.week)
		for matchup in weekMatchups:
			if matchup['user_id'] in matchupScores.keys():
				matchup['total_pts'] = matchupScores[matchup['user_id']]
			else:
				matchup['total_pts'] = 0
		return str(getTemplateSystem(session, filters).scoreboard(weekMatchups))	

class Game:
	def GET(self, gameId):
		session = web.config._session
		gameTeamsMap, weekId = auctionDb.getGameTeams(gameId)
		for userId in gameTeamsMap.keys():
			gameTeamsMap[userId]['lineup'] = auctionDb.getTeamPerformances(userId, weekId)
		return str(getTemplateSystem(session).game(gameTeamsMap))
