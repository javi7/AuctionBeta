function changeKeep(e) {
	var keepCell = e.target.getParent('td');
	var keep = keepCell.getElement('button').get('text') == 'Unkeep' ? 0 : 1;
	var keepPost = new Request({
		url: '/api/keep',
		method: 'post',
		data: {
			'playerId': keepCell.get('playerId'),
			'keep': keep,
			'weekId': $$('select[name="week"]').get('value')[0]
		},
		onSuccess: function(data) {
			data = JSON.decode(data);
			if (data['success'] == true) {
				var button = keepCell.getElement('button')
				var keepText = button.get('text') == 'Unkeep' ? 'Keep' : 'Unkeep';
				button.set('text', keepText);
				if (keepText == 'Keep') {
					button.set('class', 'btn btn-primary btn-keep')
				} else {
					button.set('class', 'btn btn-danger btn-keep')
				}
			} else {
				alert(data['failure'])
			}
		},
		onFailure: function() {
			alert('website oops! tell Javi!');
		}
	});
	keepPost.post();
}