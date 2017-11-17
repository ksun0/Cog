/**
    This is an OOP enclosure of a Task.
    It inherits from Job. Eventually, all
    Task specific processing should take
    place here.
**/
class Task extends Job {
    constructor(title, priority, description, uuid, unit, total_time, created_at, c_number, start_time, end_time) {
        
        super(title, description, start_time, end_time, created_at, uuid);
        this.started = (start_time === "None") ? false : true
        this.completed = (end_time === "None") ? false : true
        this.update(title, priority, description, uuid, unit, total_time, created_at, c_number, start_time, end_time);
    }
    update(title, priority, description, uuid, unit, total_time, created_at, c_number, start_time, end_time) {
        this.priority = priority;
        this.c_number = c_number;
        this.unit = unit;
        this.total_time = total_time;
        super.update(title, description, start_time, end_time, created_at, uuid);
    }
}
