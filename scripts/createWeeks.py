import web

SQL_INSERT_WEEK = "INSERT INTO t_weeks (week_number, season_year) VALUES($weekNum, 2013)"

db = web.database(dbn='mysql', db='AuctionBeta', user='root')

db.query('DELETE FROM t_weeks')
db.query('ALTER TABLE t_weeks AUTO_INCREMENT=1')

for week in range(15):
	db.query(SQL_INSERT_WEEK, vars={'weekNum': week + 1})