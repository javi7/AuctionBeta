import csv
import web

db = web.database(dbn='mysql', db='AuctionBeta', user='root')

ADD_START_DATE_QUERY = "UPDATE t_weeks SET week_start=$start WHERE week_id=$week"
ADD_END_DATE_QUERY = "UPDATE t_weeks SET week_end=$end WHERE week_id=$week"

f = open('weekDates.csv', 'rU')
csvReader = csv.reader(f)

week = 1

for row in csvReader:
	db.query(ADD_START_DATE_QUERY, vars={'week': week, 'start': row[0]})
	db.query(ADD_END_DATE_QUERY, vars={'week': week, 'end': row[1]})
	week = week + 1

f.close()