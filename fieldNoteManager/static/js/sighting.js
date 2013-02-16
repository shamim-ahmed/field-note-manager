/* obs addition related js goes here */

$(document).ready(function() {
	$("#obsfield").keyup(function(event) {
	  if (event.keyCode == 13) {
	    $("#obsbutton").click();
	  }
	});
	
	$("#obsbutton").click(function() {
		$("#obsErrId").text('');
		
		var excurId = $("#excurId").text();
		var species = $("#obsfield").val();
		
		if (excurId != '' && species != '') {
			$.post("/fieldNoteManager/addSighting/", {
				excursionId : excurId,
				species : species
			}, function(data) {
				$("#obslist").append("<li>" + species + "</li>");
			});
		} else if (species == '') {
			$("#obsErrId").text("Please sepcify your observation");
		}
		
		$("#obsfield").val("");
	});
});