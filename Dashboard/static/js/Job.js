/**
    This is an OOP enclosure of a Job.
    It inherits from Job. Eventually, all
    Job specific processing should take
    place here.
**/
class Job {
    constructor(title, description, start_time, end_time, created_at, uuid) {
        this.update(title, description, start_time, end_time, created_at, uuid);
    }
    editJob () {
        
    }
    update(title, description, start_time, end_time, created_at, uuid) {
        this.title = title;
        this.start_time = start_time;
        this.end_time = end_time;
        this.description = description;
        this.created_at = created_at;
        this.uuid = uuid;
        this.started = false;
    }
}