import auctionDb

def processWeeklyBids(weekId):
	statusMap, boughtPlayersList = processOwnedPlayers(weekId)
	allBids = auctionDb.getBidsForProcessing(weekId)
	index = 0
	while (index < len(allBids)):
		bid = allBids[index]
		index += 1
		validBid, statusMap = isValidBid(bid, statusMap, boughtPlayersList)
		if not validBid:
			continue
		playerBidList = [bid]
		while index < len(allBids) and allBids[index]['player_id'] == bid['player_id'] and \
				allBids[index]['bid_amount'] == bid['bid_amount']:
			validBid, statusMap = isValidBid(allBids[index], statusMap, boughtPlayersList)
			if validBid:
				playerBidList.append(allBids[index])
			index += 1
		playerAdded, statusMap = arbitrateBid(playerBidList, statusMap)
		if playerAdded:
			boughtPlayersList.append(bid['player_id'])
	createLineups(statusMap, weekId)
	return statusMap

def processOwnedPlayers(weekId):
	statusMap = {}
	ownedPlayers = auctionDb.getAllOwnedPlayers(weekId)
	ownedPlayerIds = []
	for player in ownedPlayers:
		if player['user_id'] not in statusMap.keys():
			statusMap[player['user_id']] = { 'budget': 100}
		success, statusMap = arbitrateBid([player], statusMap)
		ownedPlayerIds.append(player['player_id'])
	return statusMap, ownedPlayerIds

def isValidBid(bid, statusMap, boughtPlayersList):
	userId = bid['user_id']
	if bid['player_id'] in boughtPlayersList:
		return False, statusMap
	if userId not in statusMap.keys():
		statusMap[userId] = { 'budget': 100 }
	if not isValidBudget(bid, statusMap[userId]):
		return False, statusMap
	elif not isValidRoster(bid, statusMap[userId]):
		return False, statusMap
	return True, statusMap

def isValidBudget(bid, userMap):
	mapKeys = userMap.keys()
	mapKeys.remove('budget')
	rosterSize = 0
	for mapKey in mapKeys:
		rosterSize += len(userMap[mapKey])
	playersNeeded = 5 - rosterSize - 1
	if bid['bid_amount'] > userMap['budget'] - playersNeeded:
		return False
	return True 

def isValidRoster(bid, userMap):
	position = bid['player_position']
	if position == 'TE':
		position = 'WR'
	if position not in userMap.keys():
		return True
	elif position == 'QB' or len(userMap[position]) > 1:
		return False
	return True

def arbitrateBid(playerBidList, statusMap):
	bid = playerBidList[0]
	position = bid['player_position']
	if position not in statusMap[bid['user_id']].keys():
		statusMap[bid['user_id']][position] = []
	statusMap[bid['user_id']][position].append(bid['player_id'])
	statusMap[bid['user_id']]['budget'] -= bid['bid_amount']
	return True, statusMap

def createLineups(statusMap, weekId):
	for userId in statusMap.keys():
		print str(statusMap[userId])
		players = []
		for positionKey in statusMap[userId].keys():
			if positionKey in ['QB', 'RB', 'WR']:
				for player in statusMap[userId][positionKey]:
					players.append(player)
		auctionDb.setNewLineup(userId, weekId, players)