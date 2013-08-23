import auctionDb

users = ['a','b','c','d','e','f','g','h']

for user in users:
	auctionDb.register(user, user, user)