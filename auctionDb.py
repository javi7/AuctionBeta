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

SELECT_NFL_PLAYERS_FOR_BIDDING_HEAD = 'SELECT np.*, b1.player_id as bid_player_id, '+\
										'b1.bid_amount, l.user_id as owner_id, su.user_alias as owner_name, ' +\
										'b2.bid_amount as winning_bid FROM t_nfl_players np LEFT JOIN t_bids b1 ' +\
										'ON b1.player_id=np.player_id AND b1.user_id=$userId ' +\
										'AND b1.bid_status=1 ' +\
										'AND b1.week_id=$weekId LEFT JOIN (t_lineup_players lp JOIN t_lineups l ' +\
										'JOIN t_site_users su) ON (lp.player_id=np.player_id AND ' +\
										'l.lineup_id=lp.lineup_id AND l.week_id=$weekId AND ' +\
										'su.user_id=l.user_id) LEFT JOIN t_bids b2 ON b2.user_id=su.user_id ' +\
										'AND b2.week_id=$weekId AND b2.bid_status=1 AND b2.player_id=b1.player_id ' +\
										'WHERE player_position IN $positionList '

SELECT_NFL_PLAYERS_BIDDING_FOOT = 'AND player_name LIKE $search ' +\
									'ORDER BY player_wkal_points DESC, bid_amount DESC LIMIT 50 ' +\
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
				'AND lp.player_id=b.player_id AND l.week_id=b.week_id and b.bid_status=1'

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

SELECT_GAMES_BY_WEEK = 'SELECT m.*, u.user_alias, u.user_id FROM t_matchups m JOIN t_games g ON m.game_id=g.game_id ' +\
						' JOIN t_site_users u ON u.user_id=m.user_id WHERE g.week_id=$weekId ORDER BY game_id DESC, u.user_alias ASC'

SELECT_WEEK_DATES = 'SELECT week_start, week_end FROM t_weeks WHERE week_id=$weekId'

SELECT_ALL_NFL_PLAYERS = 'SELECT * FROM t_nfl_players'

INSERT_NEW_PERFORMANCE = 'INSERT INTO t_performances $fields VALUES $values'

DELETE_PERFORMANCE = 'DELETE FROM t_performances WHERE player_id=$playerId AND week_id=$weekId'

SELECT_PERFORMANCE = 'SELECT * FROM t_performances WHERE player_id=$playerId AND week_id=$weekId'

SELECT_LINEUP_PERFORMANCES = 'SELECT p.*, np.player_name, np.player_position FROM t_lineup_players lp JOIN t_lineups l ' +\
								'ON l.lineup_id=lp.lineup_id ' +\
								'AND l.user_id=$userId AND l.week_id=$weekId JOIN t_nfl_players np ON ' +\
								'np.player_id=lp.player_id LEFT JOIN t_performances p ' +\
								'ON lp.player_id=p.player_id ORDER BY np.player_position ASC, np.player_id DESC'

SELECT_MATCHUP_TEAM_SCORES = 'SELECT SUM(p.total_pts) AS total_pts, l.user_id FROM t_performances p JOIN t_lineup_players lp ' +\
								'ON lp.player_id=p.player_id JOIN t_lineups l ON l.lineup_id=lp.lineup_id AND l.week_id=$weekId ' +\
								'GROUP BY l.user_id'

SELECT_GAME_TEAMS = 'SELECT u.user_alias, u.user_id, g.week_id FROM t_games g JOIN t_matchups m ON g.game_id=m.game_id JOIN t_site_users u ' +\
					'ON u.user_id=m.user_id WHERE g.game_id=$gameId'

SELECT_GET_ALL_KEEPERS = 'SELECT lp.*, l.user_id, b.bid_amount FROM t_lineup_players lp JOIN t_lineups l ON l.lineup_id=lp.lineup_id ' +\
							'AND l.week_id=$weekId JOIN t_bids b ON b.user_id=l.user_id AND b.player_id=lp.player_id AND b.bid_status=1 ' +\
							'AND b.week_id=l.week_id WHERE lp.lineup_player_keep=1 ORDER BY l.user_id ASC'

SELECT_LINEUP_PLAYER = 'SELECT * FROM t_lineup_players lp JOIN t_lineups l ON lp.lineup_id=l.lineup_id AND l.week_id=$weekId ' +\
						'WHERE lp.player_id=$playerId'

UPDATE_NFL_PLAYER_WKAL_POINTS = 'UPDATE t_nfl_players SET player_wkal_points = player_wkal_points + $points ' +\
								'WHERE player_id=$playerId'

UPDATE_ADD_USER_WIN = 'UPDATE t_site_users SET user_wins = user_wins + 1 WHERE user_id=$userId'
UPDATE_ADD_USER_LOSS = 'UPDATE t_site_users SET user_losses = user_losses + 1 WHERE user_id=$userId'
UPDATE_ADD_USER_TIE = 'UPDATE t_site_users SET user_ties = user_ties + 1 WHERE user_id=$userId'
UPDATE_USER_POINTS_FOR = 'UPDATE t_site_users SET user_points_for = user_points_for + $points WHERE user_id=$userId'

SELECT_USERS_FOR_STANDINGS = 'SELECT * FROM t_site_users ORDER BY user_division DESC, user_wins DESC, user_points_for DESC'

dbase = db.database(dbn='mysql', db='AuctionBeta', user='root')

def query(queryString, queryParams):
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

def setNewLineup(userId, weekId, playerIdList):
	lineupResult = query(SELECT_LINEUP_ID, {
		'userId': userId, 'weekId': weekId
	})
	if not lineupResult:
		query(INSERT_NEW_LINEUP, {
			'userId': userId, 'weekId': weekId
		})
		lineupResult = query(SELECT_LINEUP_ID, {
			'userId': userId, 'weekId': weekId
		})
	lineupId = lineupResult[0]['lineup_id']
	for playerId in playerIdList:
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
	return weekMatchupsResult.list()

def getWeekDates(weekId):
	weekDatesResult = query(SELECT_WEEK_DATES, {
		'weekId': weekId
	})
	return weekDatesResult[0]

def getNflPlayers():
	nflPlayersResult = query(SELECT_ALL_NFL_PLAYERS, {})
	return nflPlayersResult.list()

def setNewPerformance(performanceMap):
	newPerformanceQuery = dbase.multiple_insert('t_performances', values=[performanceMap])
	print newPerformanceQuery

def getPerformance(playerId, weekId):
	performanceResult = query(SELECT_PERFORMANCE, {
		'playerId': playerId, 'weekId': weekId
	})
	if performanceResult:
		return performanceResult[0]
	else:
		return None

def removePerformance(playerId, weekId):
	removePerformanceResult = query(DELETE_PERFORMANCE, {
		'playerId': playerId, 'weekId': weekId
	})

def getTeamPerformances(userId, weekId):
	teamPerformanceResult = query(SELECT_LINEUP_PERFORMANCES, {
		'userId': userId, 'weekId': weekId
	})
	return teamPerformanceResult.list()

def getMatchupScores(weekId):
	matchupScoresResult = query(SELECT_MATCHUP_TEAM_SCORES, {
		'weekId': weekId
	})
	matchupScoresMap = {}
	for score in matchupScoresResult:
		matchupScoresMap[score['user_id']] = score['total_pts']
	return matchupScoresMap

def getGameTeams(gameId):
	gameTeamsResult = query(SELECT_GAME_TEAMS, {
		'gameId': gameId
	})
	gameTeamsMap = {}
	weekId = 0
	for team in gameTeamsResult:
		weekId = team['week_id']
		gameTeamsMap[team['user_id']] = {'teamName': team['user_alias']}
	return gameTeamsMap, weekId

def getAllKeepers(weekId):
	keepersResult = query(SELECT_GET_ALL_KEEPERS, {
		'weekId': weekId
	})
	return keepersResult.list()

def addWkalPoints(playerId, points):
	wkalPointsResult = query(UPDATE_NFL_PLAYER_WKAL_POINTS, {
		'playerId': playerId, 'points': points
	})

def addUserResult(userId, result, points):
	if result == 'win':
		queryString = UPDATE_ADD_USER_WIN
	elif result == 'loss':
		queryString = UPDATE_ADD_USER_LOSS
	elif result == 'tie':
		queryString = UPDATE_ADD_USER_TIE
	else:
		return None
	userResultResult = query(queryString, {'userId': userId})
	userPointsResult = query(UPDATE_USER_POINTS_FOR, {
		'userId': userId, 'points': points
	})

def getStandingsList():
	standingsResult = query(SELECT_USERS_FOR_STANDINGS, {})
	return standingsResult.list()