// Adding remove property to array for throwError
Array.prototype.remove = function() {
    var what, a = arguments, L = a.length, ax;
    while (L && this.length) {
        what = a[--L];
        while ((ax = this.indexOf(what)) !== -1) {
            this.splice(ax, 1);
        }
    }
    return this;
};
/**
    All universal utility functions are here.
    No page specific functions should be here.
**/
var c_errors = []
function throwError(title, message) {
    if (title==""){
        title = "Error!"
    }
    var errId = "errorNotification_"+guid()
    var div = '<div class="alert alert-danger errorMessage" id="'+errId+'"><strong>'+title+'</strong><br>'+message+'</div>'
    $('body').prepend(div)
    var margin = 5;
    for (var i = 0; i <c_errors.length; i++) {
        var id = c_errors[i];
        $("#"+id).css({top: $("#"+id).offset()["top"]+margin+$("#"+errId).outerHeight()});
    }
    c_errors.push(errId);
    setTimeout(function() {$("#"+errId+"").fadeOut(500, function() { $(this).remove(); c_errors.remove(errId)});}, 2000)
}
function parseQuery(qstr) {
    var query = {};
    var a = (qstr[0] === '?' ? qstr.substr(1) : qstr).split('&');
    for (var i = 0; i < a.length; i++) {
        var b = a[i].split('=');
        query[decodeURIComponent(b[0])] = decodeURIComponent(b[1] || '');
    }
    return query;
}
function parseEvents(events) {
    for (var i = 0; i < events.length; i++) {
        try {
            var event_data = JSON.parse(events[i]);
            events[i] = new Event(event_data["Title"],
                                event_data["Description"],
                                event_data["Creation Date"],
                                event_data["Start Time"],
                                event_data["End Time"],
                                event_data["unique_id"])
        } catch(e) {
            console.log("Unparsable event");
            console.log(event_data);
        }
    }
    return events
}
function parseTasks(tasks) {
    for (var i = 0; i < tasks.length; i++) {
        try {
            var task_data = JSON.parse(tasks[i]);
            tasks[i] = new Task(task_data["Title"],
                                task_data["Priority"],
                                task_data["Description"],
                                task_data["unique_id"],
                                task_data["Unit"],
                                task_data['Total Time'],
                                task_data["created_at"],
                                task_data["c_number"]);
        } catch(e) {
            console.log("Unparsable task: ", e);
            console.log(task_data);
        }
    }
    return tasks
}
function parseSecondsToTimeString(time) {
    return parseInt(parseFloat(time)/60/60) + ":" + (parseFloat(time)/60%60 < 10 ? "0" : "") + parseFloat(time)/60%60;
}
function guid() {
  function s4() {
    return Math.floor((1 + Math.random()) * 0x10000)
      .toString(16)
      .substring(1);
  }
  return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
    s4() + '-' + s4() + s4() + s4();
}
function timeToRadians(timeStr) {
    var d = new Date(timeStr);
    var reference = new Date();
    reference.setHours(0, 0, 0, 0);
    var time = (d.getTime() - reference) / 1000 / 60 / 60
    return ((time)) / 12 * 2 * Math.PI;
}
function decode(str) {
    var encodedStr = str;
    var parser = new DOMParser;
    var dom = parser.parseFromString(
        '<!doctype html><body>' + encodedStr,
        'text/html');
    var decodedString = dom.body.textContent;
    return decodedString;
}
function addHeaderDate() {
    var dayarray = new Array("SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT");
    var montharray = new Array("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC");
    var mydate = new Date();
    var year = mydate.getFullYear();
    var day = mydate.getDay();
    var month = mydate.getMonth();
    var daym = mydate.getDate();
    if (daym < 10)
        daym = "0" + daym;
    if (document.getElementById("HeaderDate")){
        document.getElementById("HeaderDate").innerHTML += "<h1 style='color: #FFF; font-size:50px; margin-top:20px;'>" + dayarray[day] + "</h1>";
        document.getElementById("HeaderDate").innerHTML += "<h4 style='color:#FFF; margin-left:5px; margin-top:-10px;'>" + montharray[month] + " " + daym + "</h4>";
    }
}