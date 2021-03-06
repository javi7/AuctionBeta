function login(e) {
	e.preventDefault();
	var form = e.target.getParent('form');
	var loginPost = new Request({
		url: '/ajax/login',
		method: 'post',
		data: {
			'username': form.getElement('input[name="username"]').get('value'),
			'password': form.getElement('input[name="password"]').get('value')
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

function logout(e) {
	e.preventDefault();
	var logoutPost = new Request({
		url: '/ajax/logout',
		method: 'post',
		onSuccess: function(data) {
			data = JSON.decode(data);
			if (data['success']) {
				window.location.assign(window.location.origin);
			} else {
				alert('Website oops! Tell Javi!');
			}
		},
		onFailure: function() {
			alert('Website oops! Tell Javi!')
		}
	});
	logoutPost.post();
}