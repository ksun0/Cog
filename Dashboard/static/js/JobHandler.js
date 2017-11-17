/**
    This encloses all jobs and events.
    Unlike the classes, it	should be referenced
    only statically.
**/
class JobHandler {
	static getJobs(retFunc) {
		JobHandler.hasLoaded = true;
		_getJobs(
			function (jobs){
				JobHandler._tasks = []
				JobHandler._events = []
				Array.prototype.push.apply(JobHandler._tasks, jobs[0])
				Array.prototype.push.apply(JobHandler._events, jobs[1])
				console.log(console.log('here', JobHandler._tasks))
				JobHandler.filter_by_uuid(JobHandler._tasks)
				JobHandler.filter_by_uuid(JobHandler._events)
				if (typeof retFunc !== 'undefined') {
					retFunc();
				}
			})
		this.lastUpdate = Date.now();
	}
	static filter_by_uuid(jobs) {
		// Passed a single array of either tasks or events and
		// filters out duplicates based on uuid.
		for (var i = jobs.length - 1; i >= 0; i--) {
			for (var i2 = i-1; i2 >= 0; i2--) {
				if (jobs[i].uuid === jobs[i2].uuid) {
					jobs.pop(i2)
					i--;
				}
			}
		}
	}
	static create_job_from_get(form_data) {
		var job_data = parseQuery(form_data);
		if (job_data["toggle"] == "task") {
			JobHandler.addTask(job_data["title"],
								job_data["priority"],
								job_data["description"],
								job_data["uuid"],
								job_data["unit"],
								job_data["c_number"])
		} else {
			JobHandler.addEvent(job_data["title"],
								job_data["description"],
								'',
								job_data["start"],
								job_data["end"],
								job_data["uuid"])
		}
		_createJob(job_data)
	}
	static update() {
		if (Date.now() - JobHandler.lastUpdate > JobHandler.updateRate) {
			JobHandler.lastUpdate = Date.now()
			JobHandler.getJobs()
		}
	}
	static deleteJob_from_get(form_data) {
		JobHandler.update();
		var job_data = parseQuery(form_data);
		for (var i = JobHandler._events.length-1; i >= 0; i--) {
			if (JobHandler._events[i].uuid === job_data["uuid"]) {
				JobHandler._events.pop(i)
			}
		}
		for (var i = JobHandler._tasks.length-1; i >= 0; i--) {
			if (JobHandler._tasks[i].uuid === job_data["uuid"]) {
				JobHandler._tasks.pop(i)
			}
		}
		_createJob(form_data);
	}
	static get jobs() {
		JobHandler.update();
		return [JobHandler._tasks, JobHandler._events];
	}
	static get events() {
		JobHandler.update();
		return JobHandler._events;
	}
	static get tasks() {
		JobHandler.update();
		return JobHandler._tasks;
	}

	static get unitTitles() {
		JobHandler.update();
		var titles = [];
		for (var i = 0; i < JobHandler._allUnits.length; i++) {
			titles.push(JobHandler._allUnits[i]["title"]);
		}
		return titles;
	}

	static get_ratio(unit_str) {
		for (var i = 0; i < JobHandler._allUnits.length; i++) {
			if (unit_str.toUpperCase() === JobHandler._allUnits[i]["title"].toUpperCase()) {
				return JobHandler._allUnits[i]["ratio"]
			}
		}
		console.log("UNIT NOT FOUND!")
		return 1
	}

	static addTask(title, priority, description, uuid, unit, c_number, created_at="", started_at="", ended_at="") {
		var updated = false;
		var total_time = this.get_ratio(unit)*c_number;
		for (var i = 0; i < JobHandler._tasks.length; i++) {
			if (JobHandler._tasks[i].uuid == uuid) {
				console.log("Editing task");
				updated = true;
				JobHandler._tasks[i].update(title, priority, description, uuid, unit, total_time, created_at, c_number, started_at, ended_at)
			}
		}
		if (!updated) {
			console.log("Creating new task");
			JobHandler._tasks.push(new Task(title, priority, description, uuid, unit, total_time, created_at, c_number, started_at, ended_at));
		}
	}

	static addEvent(title, description, created_at, start_time, end_time, uuid) {
		var updated = false;
		for (var i = 0; i < JobHandler._events.length; i++) {
			if (JobHandler._events[i].uuid == uuid) {
				console.log("Editing event");
				updated = true;
				JobHandler._events[i].update(title, description, uuid, end_time, start_time, created_at)
			}
		}
		if (!updated) {
			console.log("Creating new event");
			JobHandler._events.push(new Event(title, description, created_at, start_time, end_time, uuid));
		}
	}
}
JobHandler._allUnits = []; // Internal representation of allUnits
JobHandler._customUnits = []; // Internal representation of Custom Units
JobHandler._tasks = []; // Internal representation of tasks
JobHandler._events = []; // Internal representation of events
JobHandler.hasLoaded = false;
JobHandler.updateRate = 100*1000;