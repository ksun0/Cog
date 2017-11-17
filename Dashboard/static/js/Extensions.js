function load_extensions(extensions, id='extension_list') {
    //Multiline string below
    var list_form = `
                    <form action="." class="form-horizontal" method="post" novalidate="" style="border-width:1px;" onsubmit="return validateModalForm()" name="modal_form" id="list_extension_form">
                    <input type="hidden" class="uuid" id="ext_uuid" value="" name="uuid"/>
                    <div class="list-group" id="extension_list">
                    </div>
                    <script type="text/javascript">
                        handler = null;
                        $(document).ready( function () {
                            $("#list_extension_form").on("submit", function(e){
                                    exthandler.post({'uuid': $("#ext_uuid").attr("value"), "extension_selected": true})
                                    e.preventDefault();
                                    return false;
                                });
                            });
                    </script>
                </form>
                `
    $("#extension_modal").html(list_form);
    ext_str = "";
    for (var i = 0; i < extensions.length; i++) {
        var js = "$('#ext_uuid').attr('value', '"+extensions[i]["uuid"]+"'); $(this).submit();"
        ext_str += '<a onclick="'+js+'" class="list-group-item list-group-item-action flex-column align-items-start">\n<div class="d-flex w-100 justify-content-between">\n<h5 class="mb-1">';
        ext_str += extensions[i]["Title"];
        ext_str += '</h5>\n</div>\n<p class="mb-1">';
        ext_str += extensions[i]["Description"];
        ext_str += '<label style="display: hidden"></label>'
        ext_str += '</p>\n</a>\n';
    }
    $("#"+id).html(ext_str)
}

function load_sidebar_extension_list() {
    var innerHTML = "";
    for (var i = 0; i < ExtensionHandler.sidebar_extensions.length; i++) {
        var title = ExtensionHandler.sidebar_extensions[i]["Title"];
        var uuid = ExtensionHandler.sidebar_extensions[i]["uuid"];
        innerHTML += "<li class='list-group-item' onclick=\"load_sidebar_extension_selection('"+uuid+"');\">"+title+"</li>";
    }
    $("#extension_sidebar").html(innerHTML);
}

function load_sidebar_extension_selection(uuid) {
    function put_in_view(innerHTML) {
        changeToExtensionSettings()
        $("#extensions_settings").html(innerHTML);
    }
    _getExtensionSettings(put_in_view, uuid)
}
