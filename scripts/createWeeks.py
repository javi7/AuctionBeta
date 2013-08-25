import web

SQL_INSERT_WEEK = "INSERT INTO t_weeks (week_number, season_year) VALUES($weekNum, 2013)"

db = web.database(dbn='mysql', db='AuctionBeta', user='root')

for week in range(15):
	db.query(SQL_INSERT_WEEK, params={'weekNum': week + 1})