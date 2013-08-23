function filter() {
	event.preventDefault();
	var filteredUrl = window.location.pathname + '?'
	var caller = event.target;
	if (caller.get('name') != 'clearSearch') {
		if (caller.get('name') == 'search' || caller.get('class') == 'form-inline') {
			caller = $("js_search_filter");
		}
		filteredUrl += caller.get("name") + '=' + caller.get('value');
	} else {
		caller = $("js_search_filter");
	}
	var prevUrl = window.location.toString();
	var index = String.lastIndexOf(prevUrl, '?');
	if (index > 0) {
		var prevParams = prevUrl.substring(index + 1, prevUrl.length);
		var paramArray = String.split(prevParams,'&');
		for (var i = 0; i < paramArray.length; i++) {
			var param = paramArray[i];
			if (param.substring(0, param.indexOf('=')) == caller.get('name')) {
				continue;
			} else {
				filteredUrl += '&' + param;
			}
		}	
	}
	window.location = filteredUrl;
}