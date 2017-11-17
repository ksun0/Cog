class ExtensionHandler {
	constructor(render_in) {
		ExtensionHandler.jquery_selection = render_in;
	}
	static _renderIn(content) {
		// Redirect if redirect is requested
		if (typeof content === "object") {
			if ('redirect' in content) {
				content = '<iframe src="'+content['redirect']+'" onLoad="iframeDidLoad();"></iframe>';
			} else if ('newtab' in content) {
				var win = window.open(content['newtab'], '_blank');
				win.focus();
			} else if('close_modal' in content) {
				$("#extensions").modal('toggle');
				reloadGraphData()
			}
		}
		$(ExtensionHandler.jquery_selection).html(content);
	}
	post(data={}) {
		data = JSON.stringify(data);
		// Calls ajax request with get data
		// that triggers rendering in selection.
		_extension_post({
			 "csrfmiddlewaretoken": csrf_token,
			 "data": data
			},
			function(xml) {
				ExtensionHandler._renderIn(xml)
			}
		)
	}
}
ExtensionHandler.extensions = [];
ExtensionHandler.sidebar_extensions = [];
 _getExtensions(function(extensions) {
 					extensions.forEach(
 						function(x){
 							ExtensionHandler.extensions.push(x[0]);
 							if (x[1]) {
 								ExtensionHandler.sidebar_extensions.push(x[0]);
 							}
 						})
 				});
 exthandler = new ExtensionHandler("#extension_modal");