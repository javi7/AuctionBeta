from bs4 import BeautifulSoup
import requests
import re
import web

SQL_INSERT = 'INSERT INTO t_nfl_players VALUES' +\
				'($playerId, $playerName, $playerPosition, $playerNflTeam, $playerProjection)'

SQL_SELECT = 'SELECT * FROM t_nfl_players WHERE player_id=$playerId'

def buildUrl(positionId, offset):
	return 'http://games.espn.go.com/ffl/freeagency' + \
			'?leagueId=36878&seasonId=2013&avail=-1&view=projections&slotCategoryId=' + \
			str(positionId) + '&startIndex=' + str(offset) 

def playerExists(playerId):
	player = db.query(SQL_SELECT, vars={'playerId': playerId})
	if len(player) == 1:
		return True
	elif len(player) > 1:
		print len(player)
		return True
	else:
		return False

positionIdMap = { 0: 'QB', 2: 'RB', 4: 'WR', 6: 'WR' }
db = web.database(dbn='mysql', db='AuctionBeta', user='root')

for positionId in positionIdMap.keys():
	offset = 0
	url = buildUrl(positionId, offset)
	print url
	playerSoup = BeautifulSoup(requests.get(url).text)
	playerElements = playerSoup.findAll('td', 'playertablePlayerName')
	while len(playerElements):
		for player in playerElements:
			queryParams = {}
			queryParams['playerName'] = player.find('a', tab='null').text
			playerInfoRegEx = '.*, ([A-Za-z]{2,3})[\s|\xc2\xa0](QB|RB,WR|RB|WR|TE|K)[\xc2\xa0]*(P|Q|D|IR|O)?'
			queryParams['playerPosition'] = positionIdMap[positionId]
			playerInfo = re.match(playerInfoRegEx, player.text, re.S)
			queryParams['playerNflTeam'] = playerInfo.group(1)
			queryParams['playerId'] = player.find('a', tab='null')['playerid']
			queryParams['playerProjection'] = player.findParent().find('td', 'appliedPoints').text
			if not playerExists(queryParams['playerId']):
				db.query(SQL_INSERT, vars=queryParams)

		offset += 50
		url = buildUrl(positionId, offset)
		print url
		playerSoup = BeautifulSoup(requests.get(url).text)
		playerElements = playerSoup.findAll('td', 'playertablePlayerName')

