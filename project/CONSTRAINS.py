from DATA import consecutive_blocks

def process_schedule_validation(existing_schedule, weekday, timeslots, venue_obj, group_id, course_code, mode_type, remaining_count, instructor_id=""):
    for record in existing_schedule:
        if record["day"] == weekday:
            if (record["room"] == venue_obj.room_no or record["section"] == group_id or record.get("faculty") == instructor_id):
                if any(s in record["periods"] for s in timeslots):
                    return False, "Conflict", []
    return True, "Valid", []
