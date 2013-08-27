function register(e) {
	e.preventDefault();
	var form = e.target.getParent('form');
	var pw1 = form.getElement('input[name="pw1"]').get('value');
	var pw2 = form.getElement('input[name="pw2"]').get('value');
	if (pw1 != pw2) {
		alert("passwords don't match foo!");
	} else {
		var email = form.getElement('input[name="email"]').get('value');
		var teamName = form.getElement('input[name="user"]').get('value');
		var registerPost = new Request({
			url: '/ajax/register',
			method: 'post',
			data: {
				'email': email,
				'username': teamName,
				'password': pw1
			},
			onSuccess: function(data) {
				data = JSON.decode(data);
				if (data['success'] == true) {
					alert('cool, MAN! try signing in!');
					window.location = window.location;
				} else {
					alert('no tiki, no laundry. invalid e-mail address');
				}
			},
			onFailure: function(data) {
				alert('website oops! tell Javi!');
			}
		});
		registerPost.post();
	}
}