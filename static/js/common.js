function login() {
	event.preventDefault();
	var form = event.target.getParent('form');
	var loginPost = new Request({
		url: '/ajax/login',
		method: 'post',
		data: {
			'username': form.getElement('input[name="username"').get('value'),
			'password': form.getElement('input[name="password"').get('value')
		},
		onSuccess: function(data) {
			data = JSON.decode(data)
			if (data['success']) {
				window.location = window.location;
			} else {
				alert('"You are not who we thought you were. We will not let you off the hook."\nRegards,\nDennis Green');
			}

		},
		onFailure: function() {
			alert('Website oops! Tell Javi!')
		}
	});
	loginPost.post();
}

function logout() {
	
}