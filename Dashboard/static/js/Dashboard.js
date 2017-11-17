/***
This file should only contain those functions specific to
the Dashboard: mostly gui stuff. The rest has been moved
to other files.
***/
function changeToDashboard() {
    /*
    Changes the dashboard to view of main graph
    */
    $("#taskListContentDiv").hide();
    $("#eventListContentDiv").hide();
    $("#customUnitListContentDiv").hide();
    $("#ExtensionSettingsWrapper").hide();
    $("#graphContentDiv").show();
    reloadGraph();
    $("#wrapper").removeClass("toggled");
    $("#hamburger-icon").removeClass("active");
}
function changeToTasks() {
    /*
    Changes the dashboard to a view of tasks
    */
    $("#graphContentDiv").hide();
    $("#eventListContentDiv").hide();
    $("#customUnitListContentDiv").hide();
    $("#ExtensionSettingsWrapper").hide();
    $("#taskListContentDiv").show();
    $("#wrapper").removeClass("toggled");
    $("#hamburger-icon").removeClass("active");
    populateTaskListTable();
}
function changeToEvents() {
    /*
    Changes the dashboard to view of events
    */

    $("#graphContentDiv").hide();
    $("#taskListContentDiv").hide();
	$("#customUnitListContentDiv").hide();
    $("#ExtensionSettingsWrapper").hide();
    $("#eventListContentDiv").show();
    $("#wrapper").removeClass("toggled");
    $("#hamburger-icon").removeClass("active");
    populateEventListTable();
}
function changeToCustomUnits() {
    /*
    Changes the dashboard to view of events
    */
    $("#graphContentDiv").hide();
    $("#taskListContentDiv").hide();
    $("#eventListContentDiv").hide();
    $("#ExtensionSettingsWrapper").hide();
    $("#customUnitListContentDiv").show();
	$("#wrapper").removeClass("toggled");
  $("#hamburger-icon").removeClass("active");
    populateCustomUnitListTable();
}
function changeToExtensionSettings() {
    /*
    Clears the center and shows the settings wrapper
    */
    $("#graphContentDiv").hide();
    $("#taskListContentDiv").hide();
    $("#eventListContentDiv").hide();
    $("#customUnitListContentDiv").hide();
    $("#wrapper").removeClass("toggled");
    $("#hamburger-icon").removeClass("active");
    $("#ExtensionSettingsWrapper").show();
}
function openTaskModal(d) {
    /*
        Opens the task modal with values.
    */
    document.getElementById('addJobButton').click();
    $('.task-form').show();
    $('.event-form').hide();
    document.getElementById('title').value=(("title" in d) ? d.title : "");
    document.getElementById('description').value=(("description" in d) ? d.description : "");
    document.getElementById('c_number').value=(("c_number" in d) ? d["c_number"] : "");
    document.getElementById('unit').value = (("unit" in d) ? d.unit : "");
    document.getElementById('uuid').value = (("uuid" in d) ? d.uuid : "");
    console.log(d);
    $("#Complete").show();
}
function openEventModal(d) {
    /*
        Opens the events modal with values.
    */
    document.getElementById('addJobButton').click();
    $('.task-form').hide();
    $('.event-form').show();
    document.getElementById('title').value=(("title" in d) ? d.title : "");
    document.getElementById('description').value=(("description" in d) ? d.description : "");
    document.getElementById('start').value=(("start_time" in d) ? d.start_time : "");
    document.getElementById('end').value=(("end_time" in d) ? d.end_time : "");
    document.getElementById('uuid').value = (("uuid" in d) ? d.uuid : "");
    $("#Complete").show();
}
function clearModal(d) {
    /*
        Opens the events modal with values.
    */
    document.getElementById('title').value="";
    document.getElementById('description').value="";
    document.getElementById('start').value="";
    document.getElementById('end').value="";
    document.getElementById('unit').value = "";
    document.getElementById('c_number').value = "";
    $("#Complete").hide()
    reload_uuids();
    $('.task-form').show();
    $('.event-form').hide();
}
function populateCustomUnitListTable(xml) {
    /*
        Populates the custom units table on the dashboard view.
    */

    var customUnits = JobHandler._customUnits;
    $("#customUnitList").find("tr:gt(0)").remove();
    if (customUnits.length == 0) {
        $("#customUnitList").append("<tr><td>No Custom Units! Try adding some?</td></tr>")
    }
    for (var i = 0; i < customUnits.length; i++) {
        $("#customUnitList").append(
            "<tr>" +
                "<td>" +
                    customUnits[i]["title"] +
                "</td>" +
                "<td>" +
                    customUnits[i]["description"] +
                "</td>" +
                "<td>" +
                    "<form action='.' method='POST'>" +
                        "<input class='btn btn-default' type='submit' value='Delete'/>" +
                        "<input type='hidden' name='action' value='delete_custom_unit'>"+
                        "<input type='hidden' name='csrfmiddlewaretoken' value='"+csrf_token+"'>"+
                        "<input type='hidden' name='title' value='"+customUnits[i].title+"'>"+
                    "</form>" +
                "</td>" +
            "</tr>"
        );
    }

}
function populateTaskListTable() {
    /*
        Populates the task table on the dashboard view.
    */

    var tasks = JobHandler._tasks;
    tasks.sort(function (a, b) {
        return (a.priority - b.priority);
    })

    function is_first_task(task) {
        return (task.priority == 1);
    }

    function is_last_task(task) {
        return (task.priority == tasks[tasks.length-1].priority);
    }

    $("#taskList").find("tr:gt(0)").remove();
    if (tasks.length == 0) {
        $("#taskList").append("<tr><td>No Tasks! Try adding some?</td></tr>")
    }
    for (var i = 0; i < tasks.length; i++) {
        $("#taskList").append(
            "<tr>" +
                "<td>" +
                    tasks[i].priority +
                "</td>" +
                "<td>" +
                    tasks[i].title +
                "</td>" +
                "<td>" +
                    tasks[i].description +
                "</td>" +
                "<td>" +
                    tasks[i].unit +
                "</td>" +
                "<td>" +
                    parseSecondsToTimeString(tasks[i].total_time) +
                "</td>" +
                "<td>" +
                    "<form action='.' method='POST'>" +
                        "<input class='btn btn-default' type='submit' value='Delete'/>" +
                        "<input type='hidden' name='action' value='delete_task'>"+
                        "<input type='hidden' name='csrfmiddlewaretoken' value='"+csrf_token+"'>"+
                        "<input type='hidden' name='uuid' value='"+tasks[i].uuid+"'>"+
                    "</form>" +
                "</td>" +
                "<td>" +
                    (is_first_task(tasks[i]) ? '' :
                     "<form action='.' method='POST'>" +
                         "<input class='btn btn-default' type='submit' value='raise'/>" +
                         "<input type='hidden' name='action' value='raise_task_priority'>"+
                         "<input type='hidden' name='csrfmiddlewaretoken' value='"+csrf_token+"'>"+
                         "<input type='hidden' name='uuid' value='"+tasks[i].uuid+"'>"+
                     "</form>") +
                    (is_last_task(tasks[i]) ? '' :
                     "<form action='.' method='POST'>" +
                         "<input class='btn btn-default' type='submit' value='lower'/>" +
                         "<input type='hidden' name='action' value='lower_task_priority'>"+
                         "<input type='hidden' name='csrfmiddlewaretoken' value='"+csrf_token+"'>"+
                         "<input type='hidden' name='uuid' value='"+tasks[i].uuid+"'>"+
                     "</form>") +
                "</td>" +
            "</tr>");
    }
}
function populateEventListTable() {
    /*
        Populates the event table on the dashboard view.
    */
    var events = JobHandler._events;
    $("#eventList").find("tr:gt(0)").remove();
    if (events.length == 0) {
        console.log("No events")
        $("#eventList").append("<tr><td>No events! Try adding some?</td></tr>")
    } else {
        for (var i = 0; i < events.length; i++) {
            $("#eventList").append(
                "<tr>" +

                    "<td>" +
                      events[i].title +
                    "</td>" +
                    "<td>" +
                      events[i].description +
                    "</td>" +
                    "<td>" +
                      events[i].start_time +
                    "</td>" +
                    "<td>" +
                      events[i].end_time +
                    "</td>" +
                    "<td>" +
                        "<form action='.' method='POST'>" +
                            "<input class='btn btn-default' type='submit' value='Delete'/>" +
                            "<input type='hidden' name='action' value='delete_event'>"+
                            "<input type='hidden' name='csrfmiddlewaretoken' value='"+csrf_token+"'>"+
                            "<input type='hidden' name='uuid' value='"+events[i].uuid+"'>"+
                        "</form>" +
                    "</td>" +
                "</tr>");
        }
    }
}
function validateModalForm() {
    /*
        Check the add form before a form is submitted.
        TO-DO: IMPLEMENT
    */
    if (document.forms["modal_form"]["title"].value == "") {
        if (document.forms["modal_form"]["title"].value == "") {

        }
    }
}

function reload_uuids() {
    // UUIDs are unique ids for the tasks and events yet to be created.
    // They prevent duplication on reload.
    var elements = document.getElementsByClassName("uuid");
    for (var i = 0; i < elements.length; i++) {
        elements[i].value = guid();
    }
}
function isAddModalEvent() {
    // To-Do: Make more robust indicator
    return Boolean($('.task-form').attr('style'));
}
function hideAddModal() {
    // To-DO: Make better transition
    $('#addJobs').hide();
    $('.modal-backdrop').hide();
}
function loadUnits() {
    $(".autocomplete").autocomplete({
        minLength: 0,
        source: JobHandler.unitTitles
    });
}
function submit_add_modal(formdata) {
    hideAddModal();
    var action = document.getElementById('modal_submit_tag').value;
    if (action === 'delete') {
        JobHandler.deleteJob_from_get(formdata)
    } else if (action === 'add_job') {
        JobHandler.create_job_from_get(formdata)
    } else {
        console.log("Unknown request: ", action, new Error().stack)
    }
    var action = document.getElementById('modal_submit_tag').value = '';
    reload_uuids();
    reloadGraph();
}
function menutoggle() {
    /*
        Toggles the sidebar back and forth
    */
    $("#wrapper").toggleClass("toggled");
    $("#hamburger-icon").toggleClass("active");
}
function reloadGraph() {
    /*
        Deletes and reloads the graph
    */
    $('svg').remove();
    createCenterChart();
}

function reloadGraphData(f=function(){}) {
    _getCustomUnits(function(xml) {
        for (var i = 0; i < xml.length; i++) {
            JobHandler._customUnits.push(xml[i])
        }
    });
    _getAllUnits(function(xml) {
        JobHandler._allUnits = xml;
        JobHandler.getJobs(createCenterChart);
    });
    f();
}

window.onload = function() {
    addHeaderDate();
    reloadGraphData();
};
window.onresize = reloadGraph;

$(function() {
    $('#toggle-div').hover(function(){ //Open on hover
        $("#wrapper").addClass("toggled");
        $("#hamburger-icon").addClass("active");
    },
    function(){ //Open on hover
    });
    $('#sidebar-wrapper').hover(
      function(){ //Open on hover
      },
      function(){ //Open on hover
          $("#wrapper").removeClass("toggled");
          $("#hamburger-icon").removeClass("active");
      });
});
