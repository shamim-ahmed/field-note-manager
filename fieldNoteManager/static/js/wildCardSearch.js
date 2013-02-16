$(document).ready(function() {
	$("#locationfield").keyup(function() {
		var location = $(this).val();
		$.get("/fieldNoteManager/wildCardSearch/", 
				{location : location}, 
				function(data) {
				  if (data == null || $.trim(data) == "") {
					data = "No Suggestions";
				  }
			      $("#suggestions").text(data);
		        }
		);
	});
	
	$("#speciesfield").keyup(function() {
		var species = $(this).val();
		$.get("/fieldNoteManager/wildCardSearch/", 
				{species : species}, 
				function(data) {
			      if (data == null || $.trim(data) == "") {
				    data = "No Suggestions";
				  }
				  $("#suggestions").text(data);
			    }
		);
	});
});
