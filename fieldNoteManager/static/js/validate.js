function validateExcursionForm() {
	var form = document.forms['excurform'];
	
	if (form == null || form == undefined) {
		return false;
	}
	
	var location = form['location'].value;
	var date = form['date'].value;
	var time = form['time'].value;
	
	document.getElementById("locationErrId").innerHTML = "";
	document.getElementById("dateErrId").innerHTML = "";
	document.getElementById("timeErrId").innerHTML = "";
	
	if (location == null || location == "") {
		document.getElementById("locationErrId").innerHTML = "location must be specified";
		return false;
	} else if (date == null || date == "") {
		document.getElementById("dateErrId").innerHTML = "date must be specified";
		return false;
	} else if (time == null || time == "") {
		document.getElementById("timeErrId").innerHTML = "time must be specified";
		return false;
	}
		
	return true;
}