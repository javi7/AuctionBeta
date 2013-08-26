function filter() {
	event.preventDefault();
	var caller = event.target;
	if (caller.get('name') != 'clearSearch') {
		if (caller.get('name') == 'search' || caller.get('class') == 'form-inline') {
			caller = $("js_search_filter");
		}
		amendUrlParams(caller.get('name'), caller.get('value'))
	} else {
		amendUrlParams('search', null)
	}
}

function amendUrlParams(name, value) {
	var filteredUrl = window.location.pathname + '?'
	if (value != null) {
		filteredUrl += name + '=' + value;
	}
	var prevUrl = window.location.toString();
	var index = String.lastIndexOf(prevUrl, '?');
	if (index > 0) {
		var prevParams = prevUrl.substring(index + 1, prevUrl.length);
		var paramArray = String.split(prevParams,'&');
		for (var i = 0; i < paramArray.length; i++) {
			var param = paramArray[i];
			if ([name, 'offset'].contains(param.substring(0, param.indexOf('=')))) {
				continue;
			} else {
				if (filteredUrl.indexOf('?') != filteredUrl.length - 1) {
					filteredUrl += '&';
				}
				filteredUrl += param;
			}
		}	
	}
	window.location = filteredUrl;
}