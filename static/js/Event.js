/**
    This is an OOP enclosure of a Event.
    It inherits from Job. Eventually, all
    Event specific processing should take
    place here.
**/
class Event extends Job {
    constructor(title, description, created_at, start_time, end_time, uuid) {
        super(title, description, start_time, end_time, created_at, uuid);
        this.update(title, description, created_at, start_time, end_time, uuid);
    }
    update(title, description, created_at, start_time, end_time, uuid) {
        super.update(title, description, start_time, end_time, created_at, uuid);
    }
}