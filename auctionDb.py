from passlib.hash import sha256_crypt
import web.db as db
from datetime import datetime

INSERT_NEW_USER = 'INSERT INTO t_site_users (user_alias, user_password, user_email)' +\
					' VALUES($username, $password, $email)'

SELECT_USER_FROM_ALIAS_OR_EMAIL = 'SELECT * FROM t_site_users WHERE user_alias=$username OR user_email=$username'

SELECT_USER_FROM_ID = 'SELECT * FROM t_site_users WHERE user_id=$userId'

SELECT_CURRENT_WEEK = 'SELECT week_id FROM t_weeks WHERE week_status=1'

SELECT_ALL_WEEKS = 'SELECT week_id FROM t_weeks WHERE season_year=2013'

SELECT_ALL_USER_NAMES = 'SELECT user_alias FROM t_site_users'

INSERT_NEW_BID = 'INSERT INTO t_bids (player_id, user_id, week_id, bid_amount, bid_time)' +\
					' VALUES($playerId, $userId, $weekId, $bidAmount, $bidTime)'

SELECT_NFL_PLAYERS_FOR_BIDDING_HEAD = 'SELECT t_nfl_players.*, b1.player_id as bid_player_id, '+\
										'b1.bid_amount, l.user_id as owner_id, su.user_alias as owner_name, ' +\
										'b2.bid_amount as winning_bid FROM t_nfl_players LEFT JOIN t_bids b1 ' +\
										'ON b1.player_id=t_nfl_players.player_id AND b1.user_id=$userId ' +\
										'AND b1.bid_status=1 ' +\
										'AND b1.week_id=$weekId LEFT JOIN t_lineup_players lp ON ' +\
										'lp.player_id=b1.player_id LEFT JOIN t_lineups l ON ' +\
										'l.lineup_id=lp.lineup_id LEFT JOIN t_site_users su ON ' +\
										'su.user_id=l.user_id LEFT JOIN t_bids b2 ON b2.user_id=su.user_id ' +\
										'AND b2.week_id=$weekId AND b2.bid_status=1 AND b2.player_id=b1.player_id ' +\
										'WHERE player_position IN $positionList '

SELECT_NFL_PLAYERS_BIDDING_FOOT = 'AND player_name LIKE $search ' +\
									'ORDER BY player_projection DESC, bid_amount DESC LIMIT 50 ' +\
									'OFFSET $offset'

AVAIL_NFL_PLAYERS = 'AND l.user_id IS NULL '
HIDE_BIDS = 'AND b1.bid_amount IS NULL '

SELECT_ALL_NFL_PLAYERS_FOR_BIDDING =  SELECT_NFL_PLAYERS_FOR_BIDDING_HEAD + SELECT_NFL_PLAYERS_BIDDING_FOOT								

SELECT_AVAIL_NFL_PLAYERS_FOR_BIDDING = SELECT_NFL_PLAYERS_FOR_BIDDING_HEAD + AVAIL_NFL_PLAYERS +\
										SELECT_NFL_PLAYERS_BIDDING_FOOT

SELECT_ALL_NFL_PLAYERS_FOR_BIDDING_HIDE_BIDS = SELECT_NFL_PLAYERS_FOR_BIDDING_HEAD + HIDE_BIDS +\
												SELECT_NFL_PLAYERS_BIDDING_FOOT

SELECT_AVAIL_NFL_PLAYERS_FOR_BIDDING_HIDE_BIDS = SELECT_NFL_PLAYERS_FOR_BIDDING_HEAD + AVAIL_NFL_PLAYERS +\
													HIDE_BIDS + SELECT_NFL_PLAYERS_BIDDING_FOOT

UPDATE_CANCEL_BID = 'UPDATE t_bids SET bid_status=0 WHERE week_id=$weekId AND player_id=$playerId ' +\
						'AND user_id=$userId'

SELECT_BIDS_FOR_PROCESSING = 'SELECT b1.*, p.player_position FROM t_bids b1 INNER JOIN t_nfl_players p ON ' +\
								'p.player_id=b1.player_id AND b1.bid_status=1 ' +\
								'WHERE b1.week_id=$weekId ORDER BY b1.bid_amount DESC, ' +\
								'b1.player_id DESC, b1.user_id DESC, b1.bid_priority DESC'

SELECT_NFL_PLAYER_POSITION = 'SELECT player_position FROM t_nfl_players WHERE ' +\
								'player_id=$playerId'

INSERT_NEW_LINEUP = 'INSERT INTO t_lineups (user_id, week_id) VALUES($userId, $weekId)'

INSERT_NEW_LINEUP_PLAYER = 'INSERT INTO t_lineup_players(lineup_id, player_id) VALUES($lineupId, $playerId)'

SELECT_LINEUP_ID = 'SELECT lineup_id FROM t_lineups WHERE user_id=$userId AND week_id=$weekId'

SELECT_LINEUP = 'SELECT np.*, b.bid_amount, lp.lineup_player_keep FROM t_lineups l JOIN t_lineup_players lp ON ' +\
				'l.lineup_id=lp.lineup_id AND l.user_id=$userId AND l.week_id=$weekId ' +\
				'JOIN t_nfl_players np on lp.player_id=np.player_id JOIN t_bids b ON l.user_id=b.user_id ' +\
				'AND lp.player_id=b.player_id AND l.week_id=b.week_id'

SELECT_CURRENT_USER_BIDS = 'SELECT t_nfl_players.*, b1.player_id as bid_player_id, '+\
									'b1.bid_amount FROM t_nfl_players JOIN t_bids b1 ' +\
									'ON b1.player_id=t_nfl_players.player_id AND b1.user_id=$userId ' +\
									'AND b1.bid_status=1 ' +\
									'AND b1.week_id=$weekId ORDER BY bid_amount DESC'

CALL_NEW_BID_PROCEDURE = 'CALL p_insert_and_update_bids($playerId, $userId, $weekId, $bidAmount, $bidTime)'

UPDATE_KEEP_PLAYER = 'UPDATE t_lineup_players lp JOIN t_lineups l ON lp.lineup_id=l.lineup_id ' +\
						'AND l.week_id=$weekId AND l.user_id=$userId SET lp.lineup_player_keep=$keep ' +\
						' WHERE lp.player_id=$playerId'

SELECT_NUM_KEEPERS = 'SELECT COUNT(*) AS count FROM t_lineup_players lp JOIN t_lineups l ON ' +\
						'lp.lineup_id=l.lineup_id AND l.user_id=$userId AND l.week_id=$weekId ' +\
						'WHERE lp.lineup_player_keep=1'

UPDATE_CHANGE_PASSWORD = 'UPDATE t_site_users SET user_password=$password WHERE user_id=$userId'

UPDATE_CHANGE_TEAM_NAME = 'UPDATE t_site_users SET user_alias=$teamName WHERE user_id=$userId'

UPDATE_CHANGE_EMAIL = 'UPDATE t_site_users SET user_email=$email WHERE user_id=$userId'

SELECT_GAMES_BY_WEEK = 'SELECT m.*, u.user_alias FROM t_matchups m JOIN t_games g ON m.game_id=g.game_id ' +\
						' JOIN t_site_users u ON u.user_id=m.user_id WHERE g.week_id=$weekId ORDER BY game_id DESC, u.user_alias DESC '

def query(queryString, queryParams):
	dbase = db.database(dbn='mysql', db='AuctionBeta', user='root')
	return dbase.query(queryString, vars=queryParams)

def register(username, password, email):
	password = sha256_crypt.encrypt(password)
	query(INSERT_NEW_USER, {
		'username': username, 'password': password, 'email':email
	})
	return True

def login(username, password):
	userResult = query(SELECT_USER_FROM_ALIAS_OR_EMAIL, {'username': username})
	if len(userResult) == 1:
		user = userResult[0]
		dbPassword = user['user_password']
		if sha256_crypt.verify(password, dbPassword):
			return user
		else:
			return None
	else:
		return None

def verifyPassword(userId, password):
	user = getUser(userId = userId)
	if sha256_crypt.verify(password, user['user_password']):
		return True
	else:
		return False

def getUser(username=None, userId=None):
	if username == None:
		userResult = query(SELECT_USER_FROM_ID, {'userId': userId})
	else:
		userResult = query(SELECT_USER_FROM_ALIAS_OR_EMAIL, {'username': username})
	return userResult[0]

def getAllTeamNames():
	teamNameResult = query(SELECT_ALL_USER_NAMES, {})
	teamNames = []
	for team in teamNameResult:
		teamNames.append(team['user_alias'])
	return teamNames

def placeBid(userId, playerId, bidAmount, weekId):
	query(CALL_NEW_BID_PROCEDURE, {
		'userId': userId, 'playerId': playerId, 'bidAmount': bidAmount,
		'weekId': weekId, 'bidTime': datetime.now()
	})

def cancelBid(userId, playerId, weekId):
	query(UPDATE_CANCEL_BID, {
		'userId': userId, 'playerId': playerId, 'weekId': weekId
	})

def getNflPlayersForBidding(userId, playerPosition, offset, weekId, search, avail, showBids):
	positionList = []
	if playerPosition != 'All':
		positionList.append(playerPosition)
	else:
		positionList = ['QB', 'RB', 'WR', 'TE']
	if avail == 'Available':
		if showBids == 'Hide':
			nflPlayerQuery = SELECT_AVAIL_NFL_PLAYERS_FOR_BIDDING_HIDE_BIDS
		else:
			nflPlayerQuery = SELECT_AVAIL_NFL_PLAYERS_FOR_BIDDING
	elif showBids == 'Hide':
		nflPlayerQuery = SELECT_ALL_NFL_PLAYERS_FOR_BIDDING_HIDE_BIDS
	else:
		nflPlayerQuery = SELECT_ALL_NFL_PLAYERS_FOR_BIDDING
	nflPlayersResult = query(nflPlayerQuery, {
		'userId': userId, 'positionList': positionList, 
		'offset': offset, 'weekId': weekId, 'search': '%' + search + '%'
	})
	nflPlayersMoreResult = query(nflPlayerQuery, {
		'userId': userId, 'positionList': positionList, 
		'offset': offset + 50, 'weekId': weekId, 'search': '%' + search + '%'
	})
	if len(nflPlayersMoreResult) > 0:
		more = True
	else:
		more = False
	return nflPlayersResult.list(), more

def getBidsForProcessing(weekId):
	bidsResult = query(SELECT_BIDS_FOR_PROCESSING, {
		'weekId': weekId
	})
	return bidsResult.list()

def getNflPlayerPosition(playerId):
	positionResult = query(SELECT_NFL_PLAYER_POSITION, {
			'playerId': playerId
	})
	return positionResult[0]['player_position']

def setNewLineup(userId, weekId, playerMap):
	players = []
	for positionKey in playerMap.keys():
		if positionKey in ['QB', 'RB', 'WR']:
			for player in playerMap[positionKey]:
				players.append(player)
	query(INSERT_NEW_LINEUP, {
		'userId': userId, 'weekId': weekId
	})
	lineupResult = query(SELECT_LINEUP_ID, {
		'userId': userId, 'weekId': weekId
	})
	lineupId = lineupResult[0]['lineup_id']
	for playerId in players:
		query(INSERT_NEW_LINEUP_PLAYER, {
			'lineupId': lineupId, 'playerId': playerId
		})

def getLineup(userId, weekId):
	lineupResult = query(SELECT_LINEUP, {
		'userId': userId, 'weekId': weekId
	})
	return lineupResult.list()

def getUserBids(userId, weekId):
	bidsResult = query(SELECT_CURRENT_USER_BIDS, {
		'userId': userId, 'weekId': weekId
	})
	return bidsResult.list()

def changePlayerKeepStatus(userId, playerId, weekId, keep):
	query(UPDATE_KEEP_PLAYER, {
		'userId': userId, 'playerId': playerId, 'weekId': weekId, 'keep': keep
	})

def getNumKeepers(userId, weekId):
	numKeepersResult = query(SELECT_NUM_KEEPERS, {
		'userId': userId, 'weekId': weekId
	})
	return numKeepersResult[0]['count']

def getCurrentWeek():
	weekResult = query(SELECT_CURRENT_WEEK, {})
	return weekResult[0]['week_id']

def getAllWeeks():
	weekResult = query(SELECT_ALL_WEEKS, {})
	weekList = []
	for week in weekResult:
		weekList.append(week['week_id'])
	return weekList

def changePassword(userId, password):
	password = sha256_crypt.encrypt(password)
	query(UPDATE_CHANGE_PASSWORD, {
		'userId': userId, 'password': password
	})

def changeEmail(userId, email):
	query(UPDATE_CHANGE_EMAIL, {
		'userId': userId, 'email': email
	})

def changeTeamName(userId, teamName):
	query(UPDATE_CHANGE_TEAM_NAME, {
		'userId': userId, 'teamName': teamName
	})

def getWeekMatchups(weekId):
	weekMatchupsResult = query(SELECT_GAMES_BY_WEEK, {
		'weekId': weekId
	})
	return weekMatchupsResult

