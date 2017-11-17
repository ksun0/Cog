/*
    This file is the entirety of the logic
    of the center graph.
*/
function started_task() {
    
}
function createTimeline() {
    /*
        Creates the timeline using. Currently this
        code is in flux.
    */
    var timeline = [],
    tasksIndex = 0,
    eventsIndex = 0,
    currentTime = Date.now(),
    pointer = currentTime;
    events = JobHandler.events
    tasks = JobHandler.tasks
    tasks.sort(function (a, b) {
        return (a.priority - b.priority);
    })

    function processTask(ta) {
        ta.start_time = new Date(pointer);
        var e = pointer + ta.total_time*1000; // total time: second --> milliseconds
        if (e > currentTime + 43200000) {
            // if the task is cut off by wrapping all the way around the wheel:
            ta.end_time = new Date(currentTime + 43200000);
        } else {
            ta.end_time = new Date(e);
        }
        pointer = new Date(ta.end_time).getTime();
        return ta;
    }

    function processEvent(ev) {
        var s = new Date(ev.start_time).getTime();
        var e = new Date(ev.end_time).getTime();
        if (s < currentTime) {
            ev.start_time = new Date(currentTime);
        }
        if (e > currentTime + 43200000) {
            // if event is cut off by wrapping all the way around the wheel
            ev.end_time = new Date(currentTime + 43200000);
        }
        pointer = new Date(ev.end_time).getTime();
        return ev;
    }

    function isInNext12Hours(ev) {
        var s = new Date(ev.start_time).getTime();
        var e = new Date(ev.end_time).getTime();
        var inNext12Hours = e > currentTime && s < currentTime + 43200000;
        return inNext12Hours;
    }

    while (eventsIndex < events.length) {
        if (tasksIndex == tasks.length) {
            while (eventsIndex < events.length) {
                if (isInNext12Hours(events[eventsIndex])) {
                    var ev = processEvent(events[eventsIndex]);
                    timeline.push(ev);
                }
                eventsIndex++;
            }
            break;
        }
        var nextStart = new Date(events[eventsIndex].start_time).getTime();
        if (nextStart - pointer >= parseInt(tasks[tasksIndex].total_time) && nextStart >= currentTime) {
            var ta = processTask(tasks[tasksIndex]);
            timeline.push(ta);
            tasksIndex++;
        } else {
            if (isInNext12Hours(events[eventsIndex])) {
                var ev = processEvent(events[eventsIndex]);
                timeline.push(ev);
            }
            eventsIndex++;
        }
    }
    while (tasksIndex < tasks.length && pointer <= currentTime + 43200000) {
        var ta = processTask(tasks[tasksIndex]);
        timeline.push(ta);
        tasksIndex++;
    }
    return timeline;
}

function createPieChart(canvas, timeline, radius, width, height, scale) {
    /*
        Creates the pi chart. All the arcs are contained in the arcContainer
        which is a sub-canvas of canvas.
    */
    var arcContainer = canvas.append("g");
    var outerRadius = 6 * radius * scale;
    var innerRadius = 5.25 * radius * scale;
    var color = d3.scaleOrdinal(d3.schemeCategory20);
    var arc = d3.arc()
        .innerRadius(innerRadius)
        .outerRadius(outerRadius)
        .startAngle(function(d) {
            return timeToRadians(d.start_time);
        })
        .endAngle(function(d) {
            return timeToRadians(d.end_time);
        });
    var arcOver = d3.arc()
    .innerRadius(innerRadius)
    .outerRadius(outerRadius + radius * scale)
    .startAngle(function(d) {
        return timeToRadians(d.start_time);
    })
    .endAngle(function(d) {
        return timeToRadians(d.end_time);
    });

    var div = d3.select(".tooltip")
        .attr("class", "tooltip")
        .style("opacity", 0);

    var arcs = arcContainer.selectAll(".arc")
        .data(timeline)
        .enter()
        .append("g")
        .attr("class", "arc")
        .attr("fill", function(d, i) {
            // A unique ID for each. If created at same time, they'll just be the same color.
            return color(i);
        })
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    d3.selectAll('.arc')
        .transition()
        .duration(0.5)
        .ease(d3.easeLinear)
        .attr("outerRadius", outerRadius);

    var divYOffset = 0;
    var divXOffset = 0;
    arcs.append("path")
        .attr("d", arc)
        .on("mouseover", function(d) {
          d3.select(this)
               .transition()
               .duration(500)
               .attr("d", arcOver);
            div.transition()
               .duration(200)
               .style("opacity", .8);
            div.html("<h3>" +
                     d.title +
                     "</h3>" +
                     "<h7>" +
                     ((d.description.length < 50) ? d.description : d.description.substring(0, 50)+"...") +
                     "</h7><h5>"+
                     (new Date(d.start_time)).toLocaleTimeString() + "-" +
                     (new Date(d.end_time)).toLocaleTimeString() +
                     "</h5>")
              //  .style("left", (d3.event.pageX - divXOffset) + "px")
              //  .style("top", (d3.event.pageY - divYOffset) + "px")
              //  .style("-webkit-transform", "translate(-100%, -100%)")
              ;
            })
        .on("mouseout", function(d) {
            d3.select(this).transition()
               .attr("d", arc);
            div.transition()
                .duration(500)
                .style("opacity", 0);
        })
        .on("mousemove", function(d) {
            // div.style("left", (d3.event.pageX - divXOffset) + "px")
            //    .style("top", (d3.event.pageY - divYOffset) + "px");
        })
        .on("click", function(d){
            clearModal();
            if(d.constructor == Task) {
                openTaskModal(d);
            } else {
                openEventModal(d);
            }
        });
}

function createGears(canvas, radius, width, height, scale) {
    /*
        Creates the gears. Everything is appended to the canvas.
        It has its own gear container for the purpose of translation.
    */
    var gearContainer = canvas.append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")")
        .style("left", 0)
        .style("top", 0);
    var x = Math.sin(2 * Math.PI / 3),
        y = Math.cos(2 * Math.PI / 3),
        speed = -radius/200,
        start = new Date(),
        gearColor = '#333',
        strokeWidth = '10'
        strokeColor = '#ccc';
    // Shadow filter!
    /*Canvas has definitions. Insided definitions is filters. One of the filters
    is a gaussian blur on the outside ring, as defined below.*/
    var defs = canvas.append("defs");
    // create filter with id #drop-shadow
    // height=130% so that the shadow is not clipped
    var filter = defs.append("filter")
        .attr("id", "drop-shadow")
        .attr("height", "130%");
    // SourceAlpha refers to opacity of graphic that this filter will be applied to
    // convolve that with a Gaussian with standard deviation 3 and store result
    // in blur
    filter.append("feGaussianBlur")
        .attr("in", "SourceAlpha")
        .attr("stdDeviation", radius/3)
        .attr("result", "blur");

    // translate output of Gaussian blur to the right and downwards with 2px
    // store result in feOffset
    filter.append("feOffset")
        .attr("in", "blur")
        .attr("dx", -radius/3)
        .attr("dy", -radius/3)
        .attr("result", "offsetBlur");

    // overlay original SourceGraphic over translated blurred opacity by using
    // feMerge filter. Order of specifying inputs is important!
    var feMerge = filter.append("feMerge");

    feMerge.append("feMergeNode")
        .attr("in", "offsetBlur")
    feMerge.append("feMergeNode")
        .attr("in", "SourceGraphic");

    //Create gears
    gearContainer.append("g")
        .attr("class", "annulus") // annulus is the outside ring.
        .datum({
            teeth: 80,
            radius: -radius * 5,
            annulus: true
        })
        .append("path")
        .style("filter", "url(#drop-shadow)")
        .attr("d", gear)
        .style("fill", gearColor)
        .style("stroke", gearColor)
        .attr("width", width)
        .attr("height", height);

    gearContainer.append("g")
        .attr("class", "sun")
        .datum({
            teeth: 16,
            radius: radius
        })
        .append("path")
        .attr("d", gear)
        .style("fill", gearColor)
        .style("stroke", gearColor);

    gearContainer.append("g")
        .attr("class", "planet1")
        .attr("transform", "translate(0,-" + radius * 3 + ")")
        .datum({
            teeth: 32,
            radius: -radius * 2
        })
        .append("path")
        .attr("d", gear)
        .style("fill", gearColor)
        .style("stroke", gearColor);

    gearContainer.append("g")
        .attr("class", "planet2")
        .attr("transform", "translate(" + -radius * 3 * x + "," + -radius * 3 * y + ")")
        .datum({
            teeth: 32,
            radius: -radius * 2
        })
        .append("path")
        .attr("d", gear)
        .style("fill", gearColor)
        .style("stroke", gearColor)
        .attr("width", width)
        .attr("height", height);


    function gear(d) {
        /*
            Creates an actual individual gear.
        */
        var tooth_height = radius/8;
        var tooth_inset = radius/4;
        var n = d.teeth,
            r2 = Math.abs(d.radius),
            r0 = r2 - tooth_height,
            r1 = r2 + tooth_height,
            r3 = d.annulus ? (r3 = r0, r0 = r1, r1 = r3, r2 + tooth_inset) : tooth_inset,
            da = Math.PI / n,
            a0 = -Math.PI / 2 + (d.annulus ? Math.PI / n : 0),
            i = -1,
            path = ["M", r0 * Math.cos(a0), ",", r0 * Math.sin(a0)];
        while (++i < n) path.push(
            "A", r0, ",", r0, " 0 0,1 ", r0 * Math.cos(a0 += da), ",", r0 * Math.sin(a0),
            "L", r2 * Math.cos(a0), ",", r2 * Math.sin(a0),
            "L", r1 * Math.cos(a0 += da / 3), ",", r1 * Math.sin(a0),
            "A", r1, ",", r1, " 0 0,1 ", r1 * Math.cos(a0 += da / 3), ",", r1 * Math.sin(a0),
            "L", r2 * Math.cos(a0 += da / 3), ",", r2 * Math.sin(a0),
            "L", r0 * Math.cos(a0), ",", r0 * Math.sin(a0));
        path.push("M0,", -r3, "A", r3, ",", r3, " 0 0,0 0,", r3, "A", r3, ",", r3, " 0 0,0 0,", -r3, "Z");
        return path.join("");
    }
    d3.timer(function() { //Update function
        var angle = (Date.now() - start) * speed,
            sunTransform = function(d) {
                return "rotate(" + 3 * angle / d.radius + ")";
            };
        planet1Transform = function(d) {
            return "rotate(-" + (angle - 3600 * radius/10) / d.radius + "), translate(" + -d.radius * (x * 1.5) + "," + -d.radius * (y * 1.5) + "), rotate(" + 5 / 2 * angle / d.radius + ")";
        };
        planet2Transform = function(d) {
            return "rotate(-" + angle / d.radius + "), translate(" + -d.radius * (x * 1.5) + "," + -d.radius * (y * 1.5) + "), rotate(" + 5 / 2 * angle / d.radius + ")";
        };
        gearContainer.selectAll(".sun")
            .attr("transform", sunTransform);
        gearContainer.select(".planet1")
            .attr("transform", planet1Transform);
        gearContainer.select(".planet2")
            .attr("transform", planet2Transform);
    });
}

function getTimeOfDay() {
    var now = new Date()
    var hr = now.getHours()
    var min = now.getMinutes()
    var sec = now.getSeconds()
    return [
        ["hour", hr + (min / 60) + (sec / 3600)],
        ["minute", min + (sec / 60)],
        ["second", sec]
    ]
}

function createClockHands(canvas, radius, width, height, scale) {
    radius = radius * 4;
    var clockContainer = canvas.append("g")
        .attr("transform", "translate(" + (width / 2 - radius) + "," + (height / 2 - radius) + ")")
        .attr("width", width)
        .attr("height", height);
    var cx = cy = radius;
    var margin = radius - 10;
    var hourTickLength = Math.round(radius * 0.2)
    var minuteTickLength = Math.round(radius * 0.075)

    function handLength(d) {
        if (d[0] == "hour")
            return Math.round(0.45 * radius)
        else
            return Math.round(0.90 * radius)
    }

    function handBackLength(d) {
        if (d[0] == "second")
            return Math.round(0.25 * radius)
        else
            return Math.round(0.10 * radius)
    }

    function rotationTransform(d) {
        var angle
        if (d[0] == "hour")
            angle = (d[1] % 12) * 30
        else
            angle = d[1] * 6
        return "rotate(" + angle + "," + cx + "," + cy + ")"
    }

    function updateHands() {
        clockContainer.selectAll("line.hand")
            .data(getTimeOfDay())
            .transition().ease(d3.easeBack)
            .attr("transform", rotationTransform)
    }
    // Create hands from dataset
    clockContainer.selectAll("line.hand")
        .data(getTimeOfDay())
        .enter()
        .append("line")
        .attr("class", function(d) {
            return d[0] + " hand"
        })
        .attr("x1", cx)
        .attr("y1", function(d) {
            return cy + handBackLength(d)
        })
        .attr("x2", cx)
        .attr("y2", function(d) {
            return radius - handLength(d)
        })
        .attr("transform", rotationTransform)
        .style("stroke", "#000")
        .style("stroke-width", "3px");
    setInterval(updateHands, 1000);
}

function drawArcs(canvas, radius, width, height, scale) {
    /*
    Creates arcs for the first time and then update them continually
    */
    arrangeArcs(canvas, radius, width, height, scale); // arrange immediately once
    setInterval(function() {
        canvas.selectAll("g").selectAll(".arc").remove();
        arrangeArcs(canvas, radius, width, height, scale);
    }, 20000);
}

function arrangeArcs(canvas, radius, width, height, scale) {
    /*
    Assign new angles to tasks&events and call createPieChart with the new angles
    */
    timeline = createTimeline();
    createPieChart(canvas, timeline, radius, width, height, scale);
}

function drawCurrentTime(canvas, r, width, height, scale) {

    var tickContainer = canvas.append("g")
        .attr("transform", "translate(" + (width / 2 - r) + "," + (height / 2 - r) + ")");

    function getTimeRadians() {
        var now = new Date();
        var hour = now.getHours() % 12;
        var min = now.getMinutes();
        var sec = now.getSeconds();
        return [(hour+(min/60)+(sec/3600))*30];
    }

    function updateTick() {
        var time_in_radians = getTimeRadians();
        tickContainer.selectAll("line.tick")
            .data(time_in_radians)
            .attr("transform", rotate);
    }

    function rotate(d) {
        var angle = d + 180;
        return "rotate("+angle+","+r+","+r+")";
    }

    tickContainer.selectAll("line.tick")
        .data(getTimeRadians())
        .enter()
        .append("line")
        .attr("class", "tick")
        .attr("x1", r)
        .attr("y1", r*6.25)
        .attr("x2", r)
        .attr("y2", r*7.3)
        .attr("transform", rotate)
        .style("stroke", "#F00")
        .style("stroke-width", "2px");

    setInterval(updateTick, 1000);
}

function createCenterChart() {
  var computedStyle = window.getComputedStyle(document.getElementById("graphContentDiv"));

  elementHeight = $('#graphContentDiv').outerHeight();  // height with padding
  elementWidth = $('#graphContentDiv').outerWidth();   // width with padding

  // elementHeight -= parseFloat(computedStyle.paddingTop) + parseFloat(computedStyle.paddingBottom);
  // elementWidth -= parseFloat(computedStyle.paddingLeft) + parseFloat(computedStyle.paddingRight);

    // CREATE BASE ELEMENTS
    var width = elementWidth,
        height = elementHeight,
        radius = Math.min(elementHeight, elementWidth)/14,
        offset = 0,
        scale = 1;

    var canvas = d3.select("#graphContentDiv").append("svg")
        .attr("width", width)
        .attr("height", height);

    createGears(canvas, radius, width, height, scale);

    createClockHands(canvas, radius, width, height, scale);

    drawCurrentTime(canvas, radius, width, height, scale);

    // CREATE CHANGING ELEMENTS
    drawArcs(canvas, radius, width, height, scale);
}
