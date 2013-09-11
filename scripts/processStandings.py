import auctionDb
from optparse import OptionParser

def main():
	parser = OptionParser()
	parser.add_option('-w', '--week', dest='week',
        help='enter week to scrape stats for')
	(options, args) = parser.parse_args()
	matchups = auctionDb.getWeekMatchups(options.week)
	scoreMap = auctionDb.getMatchupScores(options.week)
	for index in range(len(matchups)/2):
		team1 = matchups[index * 2]
		team2 = matchups[index * 2 + 1]
		team1['score'] = scoreMap[team1['user_id']]
		team2['score'] = scoreMap[team2['user_id']]
		if team1['score'] > team2['score']:
			auctionDb.addUserResult(team1['user_id'], 'win', team1['score'])
			auctionDb.addUserResult(team2['user_id'], 'loss', team2['score'])
		elif team2['score'] > team1['score']:
			auctionDb.addUserResult(team1['user_id'], 'loss', team1['score'])
			auctionDb.addUserResult(team2['user_id'], 'win', team2['score'])
		else:
			auctionDb.addUserResult(team1['user_id'], 'tie', team1['score'])
			auctionDb.addUserResult(team2['user_id'], 'tie', team2['score'])


if __name__ == '__main__':
	main()