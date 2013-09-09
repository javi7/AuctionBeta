from bs4 import BeautifulSoup
import requests
import auctionDb
from optparse import OptionParser

def rYds(yds):
	if yds < 0:
		return -1 * (yds / -10)
	else:
		return yds / 10

def pYds(yds):
	if yds < 0:
		return -1 * (yds / -25)
	else:
		return yds / 25

def tds(touchdowns):
	return touchdowns * 6

def turnovers(tos):
	return tos * -2

def ppr(receptions):
	return receptions

URL_START = 'http://espn.go.com/nfl/player/gamelog/_/id/'
URL_END = '/year/2013'

statFunctionMap = {'rush_att': None, 'rush_yds': rYds, 'skip': None, 'rush_tds': tds, 
					'receptions': ppr, 'rec_yds': rYds, 'rec_tds': tds, 'fumbles': None, 'fumbles_lost': turnovers,
					'pass_comp': None, 'pass_att': None, 'pass_yds': pYds, 'pass_tds': tds, 'pass_ints': turnovers}

rushing = ['rush_att', 'rush_yds', 'skip', 'skip', 'rush_tds']
receiving = ['receptions', 'rec_yds', 'skip', 'skip', 'rec_tds']
fumbles = ['fumbles', 'fumbles_lost']
passing = ['pass_comp', 'pass_att', 'pass_yds', 'skip', 'skip', 'skip', 'pass_tds', 'pass_ints', 'skip', 'skip']

statLists = {'RB': rushing + receiving + fumbles, 'WR': receiving + rushing + fumbles, 'QB': passing + rushing}
statLists['WR'].insert(1, 'skip')

def findGame(date, startDate, endDate):
	if not '/' in date:
		return False
	month = date.split('/')[0]
	day = date.split('/')[1]
	if month >= startDate.split('/')[0] and month <= endDate.split('/')[0] \
		and day >= startDate.split('/')[1] and day <= endDate.split('/')[1]:
		return True
	else:
		return False

def parseStats(statCells, pos):
	stats = {'total_pts': 0}
	for index in range(len(statLists[pos])):
		if statLists[pos][index] != 'skip':
			try:
				stats[statLists[pos][index]] = int(statCells[index + 3].text)
			except: 
				'error reading ' + statCells[index + 3]
			getPoints = statFunctionMap[statLists[pos][index]]
			if getPoints != None:
				stats['total_pts'] += getPoints(int(statCells[index + 3].text))
	return stats

def getStats(playerId, pos, week):
	playerPage = requests.get(URL_START + str(playerId) + URL_END).text
	playerSoup = BeautifulSoup(playerPage)
	playerStats = playerSoup.find('div', 'mod-player-stats')
	gameLogs = playerStats.findAll('tr', ['evenrow', 'oddrow'])
	dates = auctionDb.getWeekDates(week)
	for log in gameLogs:
		cells = log.findAll('td')
		if findGame(cells[0].text[4:], dates['week_start'], dates['week_end']):
			return parseStats(cells, pos)
	return None

def insertStats(playerId, stats, week):
	previousPerformance = auctionDb.getPerformance(playerId, week)
	if previousPerformance != None:
		auctionDb.removePerformance(playerId, week)
	newPerformance = stats
	newPerformance['player_id'] = int(playerId)
	newPerformance['week_id'] = int(week)
	auctionDb.setNewPerformance(newPerformance)

def main():
	parser = OptionParser()
	parser.add_option('-w', '--week', dest='week',
        help='enter week to scrape stats for')
	(options, args) = parser.parse_args()
	nflPlayersList = auctionDb.getNflPlayers()
	for player in nflPlayersList:
		position = player['player_position']
		if position == 'TE':
			position = 'WR'
		stats = getStats(player['player_id'], position, options.week)
		print player['player_name']
		print stats
		if stats:
			insertStats(player['player_id'], stats, options.week)


if __name__ == '__main__':
	main()

