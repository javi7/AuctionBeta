function changeAccount() {
	event.preventDefault();
	var form = event.target.getParent('form');
	var formType = form.get('name');
	var changeValue = form.getElement('input[name="' + formType + '"]').get('value');
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
				alert(data['failure']);
			}
		},
		onFailure: function() {
			alert('website oops! please tell javi!');
		}
	});
	accountChangePost.post();
}