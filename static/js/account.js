function changeAccount() {
	event.preventDefault();
	var form = event.target.getParent('form');
	var oldError = form.getElement('.errorMessage')
	if (oldError) {
		oldError.dispose();
	}
	var formType = form.get('name');
	var changeValue = form.getElement('input[name="' + formType + '"]').get('value');
	if (formType == 'newpassword') {
		if (changeValue != form.getElement('input[name="newpassword2"]').get('value')) {
			var errorDiv = new Element('div', {
					'class': 'control-group'
				})
				var errorLabel = new Element('p', {
					'class': 'controls', 'text': "new passwords don't match"
				})
				errorDiv.grab(errorLabel);
				form.grab(errorDiv);
			return;
		}
	}
	var password = form.getElement('input[name="password"]').get('value');
	var accountChangePost = new Request({
		url: '/ajax/changeaccount',
		method: 'post',
		data: {
			'changeValue': changeValue,
			'password': password,
			'field': formType
		},
		onSuccess: function(data) {
			data = JSON.decode(data);
			if (data['success']) {

			} else {
				var errorDiv = new Element('div', {
					'class': 'errorMessage control-group'
				})
				var errorLabel = new Element('p', {
					'class': 'controls', 'text': 'yo password be wrong'
				})
				errorDiv.grab(errorLabel);
				form.grab(errorDiv);
			}
		},
		onFailure: function() {
			alert('website oops! please tell javi!');
		}
	});
	accountChangePost.post();
}