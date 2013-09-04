import csv
import web

db = web.database(dbn='mysql', db='AuctionBeta', user='root')
CALL_NEW_MATCHUP = 'call new_matchup($week, $user1, $user2)'

testIdMap = { 'Javi': 10, 'Sean': 11, 'Kriner': 12, 'Eric': 13, 
				'Brian': 14, 'Binder': 15, 'Ben': 16, 'Cape': 17, 
				'Jake': 18, 'Kyle': 19 }
userIdMap = { 'Javi': 20, 'Sean': 21, 'Kriner': 22, 'Eric': 25, 
				'Brian': 28, 'Binder': 29, 'Ben': 30, 'Cape': 31, 
				'Jake': 32, 'Kyle': 35 }

f = open('schedule.csv', 'rU')

csvReader = csv.reader(f)

week = 1

for row in csvReader:
	if len(row) == 0:
		week = week + 1
	else:
		db.query(CALL_NEW_MATCHUP, vars={'week': week, 'user1': testIdMap[row[0]], 'user2': testIdMap[row[1]]})
		#create new Game
		#create two matchups

f.close()