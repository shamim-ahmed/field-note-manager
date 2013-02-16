function renderMap(latitude, longitude, divId) {
	var lat = parseFloat(latitude);
	var lng = parseFloat(longitude);
	var mapCenter = new google.maps.LatLng(lat, lng);
	
	var myOptions = {
		center : mapCenter,
		zoom : 12,
		mapTypeId : google.maps.MapTypeId.ROADMAP
	};
	
	var map = new google.maps.Map(document.getElementById(divId), myOptions);
	var marker = new google.maps.Marker({position: mapCenter, map: map});	
}
