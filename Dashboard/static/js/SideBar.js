function refreshSideBarAction() {
	// Resyncs the center graph events.
	$("#sideBarSync").addClass("fa-spin")
	// Dependent on Dashboard.js. Not ideal.
	reloadGraphData(function() {$("#sideBarSync").removeClass("fa-spin")})
}

function click_extensions() {
	// Load and open the extensions.
	load_extensions(ExtensionHandler.extensions);
}