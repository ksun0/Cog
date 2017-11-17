/*
This file contains queries. It should
wrap the queries to the best possible.
All parsing of queries should take place
here or in Utils, not in outside code.
*/
waiting_for = 0 // Number of requests currently waiting for
function started_request() {
    // Wait a bit before showing the loading screen.
    // Prevents jittery loading screens
    setTimeout(function() {
        if (waiting_for > 0) {
            waitingDialog.show();
        }
    }, 400);
    waiting_for += 1;
}


// Got to put ended_request at beginning of success in case
// the functions inside fail in order to prevent everlasting loading screen.
function ended_request() {
    waiting_for -= 1;
    if (waiting_for <= 0) {
        waiting_for = 0; // Just in case
        waitingDialog.hide();
        // $('.modal-backdrop').hide()
    }
}

function _getAllUnits(func) {
    /*
        Get all the task types.
        Can't be derived from tasks because not every
        task type has a job.
    */
    started_request()
    $.ajax({
        url: "api/getAllUnits/",
        success: function(xml) {
            xml.forEach(function(e) {
                            e["ratio"] = parseFloat(e["ratio"]);
                        })
            func(xml);
        },
        complete: ended_request,
    });
}

function _getCustomUnits(func) {
    /*
        Get all the task types.
        Can't be derived from tasks because not every
        task type has a job.
    */
    started_request()
    $.ajax({
        url: "api/getCustomUnits/",
        success: function(xml) {
            xml.forEach(function(e) {
                            e["ratio"] = parseFloat(e["ratio"]);
                        });
            func(xml);
        },
        complete: ended_request,
    });
}

function _createJob(job_data) {
    /*
        Creates a job
    */
    started_request()
    $.ajax({
        type: "POST",
        url: "",
        data: job_data,
        complete: ended_request,
    });
}

function _getTasks(func) {
    /*
        Gets all the tasks. DEPRECATED. Use _getJobs
    */
    started_request()
    $.ajax({
        url: "api/getTasks/",
        success: function(xml) {
            func(addTasks(xml));
        },
        complete: ended_request,
    });
}

function _getEvents(func) {
    /*
        Gets all the events. DEPRECATED. Use _getJobs
    */
    started_request()
    $.ajax({
        url: "api/getEvents/",
        success: function(xml) {
            func(parseEvents(xml));
        },
        complete: ended_request,
    });
}

function _getJobs(func) {
    /*
        Gets all the jobs.
    */
    started_request()
    $.ajax({
        url: "api/getJobs/",
        data: "",
        success: function(jobs) {
            var tasks = parseTasks(jobs[0]);
            var events = parseEvents(jobs[1]);
            func([tasks, events]);
       },
       complete: ended_request,
    });
}

function _getExtensions(func) {
    /*
        Gets all the extensions.
    */
    started_request()
    $.ajax({
        url: "api/extensions/",
        data: {'list': true},
        type: 'GET',
        success: function(extensions) {
            func(extensions);
       },
       complete: ended_request,
    });
}

function _extension_post(data, func) {
    /*
        Gets an extension step.
    */
    started_request()
    $.ajax({
        url: "api/extensions/",
        data: data,
        type: "POST",
        success: function(xml) {
            if (typeof func !== 'undefined') {
                func(xml);
            }
        },
        complete: ended_request,
    });
}

function _getExtensionSettings(func, uuid) {
    /*
        Gets an extension step.
    */
    started_request()
    $.ajax({
        url: "api/extensions/",
        data: {"csrfmiddlewaretoken": csrf_token,
                "data": JSON.stringify({"settings": true, "uuid": uuid})},
        type: "POST",
        success: function(xml) {
            func(xml);
        },
        complete: ended_request,
    });
}