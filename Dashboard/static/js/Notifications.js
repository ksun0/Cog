function makeNotification(title, body, time) {
    function displayNotification(title, body) {
      var options = {
          body: body,
          icon: '../../static/img/logo1.png'
      }
    //   var n = new Notification(title, options);
      new Notification(title, options);
    }
    var now = new Date();
    var msBeforeNotification = time - now;
    if (msBeforeNotification > 0) {
        setTimeout(function(){displayNotification(title, body)}, msBeforeNotification);
    }
}

function setEventNotifications() {
    Notification.requestPermission().then(function(result) {
        console.log('notification permission:', result);
    });
    function simplifyTime(d) {
        var hrs = d.getHours();
        var mins = d.getMinutes();
        var timeString = hrs%13 + ":" + '0'.repeat(2-mins.toString().length) + mins;
        if (hrs >= 12) {
            return (timeString+'pm');
        }
        return (timeString+'am');
    }
    function eventsToNotifications(xml) {
        for (var i = 0; i < xml.length; i++) {
            var theEvent = JSON.parse(xml[i]);
            var title = theEvent["Title"];
            var time = new Date(theEvent["Start Time"]);
            var st = simplifyTime(new Date(theEvent["Start Time"]));
            var et = simplifyTime(new Date(theEvent["End Time"]));
            var body = st + " to " + et;
            makeNotification(title, body, time);
        }
    }
    // This is an extra call that we don't need.
    // To-Do: Make sure that everything is updated at once with
    // one call.
    getEvents(eventsToNotifications);
}
