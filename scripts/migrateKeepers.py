import auctionDb
from optparse import OptionParser

def main():
	parser = OptionParser()
	parser.add_option('-w', '--week', dest='week',
        help='enter week to scrape stats for')
	(options, args) = parser.parse_args()
	keepers = auctionDb.getAllKeepers(options.week)
	for keeper in keepers:
		auctionDb.placeBid(keeper['user_id'], keeper['player_id'], keeper['bid_amount'], int(options.week) + 1)
		auctionDb.setNewLineup(keeper['user_id'], int(options.week) + 1, [keeper['player_id']])

if __name__ == '__main__':
	main()