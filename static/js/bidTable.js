function getWeekId() {
	return $$('select[name="week"]')[0].get('value')
}

function placeBid(e) {
	var bidCell = e.target.getParent('td');
	var bidAmount = bidCell.getElement('input').get('value')
	var placeBidPost = new Request({
		url: '/api/bid',
		method: 'post',
		data: {
			'playerId': bidCell.get('playerId'),
			'weekId': getWeekId(),
			'bidAmount': bidAmount
		},
		onSuccess: function(data) {
			data = JSON.decode(data);
			if (data['success'] == true) {
				bidCell.getElement(".placebiddiv").hide();
				bidCell.getElement(".editbiddiv").show();
				bidCell.getElement("input").set('value', bidAmount).set('disabled', 'disabled');
			} else {
				alert('please login to perform this funtivity :-)');
			}
		},
		onFailure: function() {
			alert('website oops! tell Javi!')
		}
	});
	if (bidAmount > 0) {
		placeBidPost.post();
	} else {
		alert('Must bid at least $1');
	}
}

function editBid(e) {
	var bidCell = e.target.getParent('td');
	bidCell.getElement(".editbiddiv").hide();
	bidCell.getElement(".placebiddiv").show();
	bidCell.getElement("input").set('disabled');
}

function cancelBid(e) {
	var bidCell = e.target.getParent('td');
	var deleteBid = new Request({
		url: '/api/bid',
		method: 'delete',
		emulation: false,
		data: {
			'playerId': bidCell.get('playerId'),
			'weekId': getWeekId()
		},
		onSuccess: function(data) {
			data = JSON.decode(data);
			if (data['success'] == true) {
				bidCell.getElement(".editbiddiv").hide();
				bidCell.getElement(".placebiddiv").show();
				bidCell.getElement("input").set('value', '1').set('disabled');
			} else {
				alert('please login to perform this funtivity :-)');
			}
		}
	});
	deleteBid.delete();
}

function formatBidsTable() {
	Array.each($$(".bidFormCell"), function(bidCell){
		if (bidCell.get('ownerId') != null) {
			bidCell.getElement(".placebiddiv").hide();
			bidCell.getElement(".editbiddiv").hide();
			ownerName = bidCell.get('ownerName');
			bidCell.getElement(".playerowneddiv").set('text', 'Owned by ' + ownerName);
			bidCell.getElement("input").set('value', bidCell.get('winningBid')).set('disabled', 'disabled');
		}
		else if (bidCell.get('bidAmount') > 0) {
			bidCell.getElement(".placebiddiv").hide();
			bidCell.getElement("input").set('value', bidCell.get('bidAmount')).set('disabled', 'disabled');
		} else {
			bidCell.getElement(".editbiddiv").hide();
		}
	})
	$$("body").show();
}