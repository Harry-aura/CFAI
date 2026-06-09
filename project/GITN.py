from project.DATA import consecutive_blocks
# ==========================================
# MANDATORY RULES (Do Not Violate)
# ==========================================

def verify_venue_availability(schedule_list, weekday, time_slots, facility_id):
    for record in schedule_list:
        if record["day"] == weekday and record["room"] == facility_id:
            if any(slot in record["periods"] for slot in time_slots):
                engaged_slots = "-".join(time_slots)
                return False, f"Venue {facility_id} busy on {weekday} {engaged_slots}"
    return True, ""


def verify_batch_availability(schedule_list, weekday, time_slots, cohort_id):
    for record in schedule_list:
        if record["day"] == weekday and record["section"] == cohort_id:
            if any(slot in record["periods"] for slot in time_slots):
                engaged_slots = "-".join(time_slots)
                return False, f"Cohort {cohort_id} has class on {weekday} {engaged_slots}"
    return True, ""


def verify_instructor_availability(schedule_list, weekday, time_slots, instructor_name):
    if not instructor_name:
        return True, ""

    for record in schedule_list:
        if record["day"] == weekday and record.get("faculty") == instructor_name:
            if any(slot in record["periods"] for slot in time_slots):
                engaged_slots = "-".join(time_slots)
                return False, f"Instructor {instructor_name} busy on {weekday} {engaged_slots}"
    return True, ""


def verify_venue_suitability(activity_cat, facility_cat):
    if activity_cat == 'P':
        if facility_cat != 'Lab':
            return False, "Practical session requires Lab"
    elif activity_cat in ['L', 'T', 'S']:
        if facility_cat != 'Theory':
            display_cat = {"L": "Lecture", "T": "Tutorial", "S": "Skill"}[activity_cat]
            return False, f"{display_cat} session requires Theory room"
    else:
        return False, f"Unknown session category: {activity_cat}"

    return True, ""


def verify_sequence_logic(time_slots, credits_left):
    if len(time_slots) == 2:
        pair = (time_slots[0], time_slots[1])
        if pair in consecutive_blocks:
            if credits_left >= 2:
                return True, ""
            else:
                return False, "Insufficient credits for a double block"
        else:
            return False, f"Slots {time_slots[0]}-{time_slots[1]} not a valid block"

    elif len(time_slots) == 1:
        if credits_left == 1:
            return True, ""
        else:
            return False, "Single slot restricted to final credit"

    return False, "Invalid slot count: Allowed 1 or 2"


def verify_workload_limit(time_slots, credits_left):
    if len(time_slots) > credits_left:
        return False, f"Cannot allocate {len(time_slots)} slots. Only {credits_left} left."
    return True, ""


# ==========================================
# PREFERENCE RULES (Optimization)
# ==========================================

def verify_daily_course_limit(schedule_list, weekday, module_code, cohort_id):
    for record in schedule_list:
        if record["day"] == weekday and record["section"] == cohort_id and record["course"] == module_code:
            return False, f"Notice: Module {module_code} repeated on {weekday}"
    return True, ""


def verify_load_distribution(schedule_list, weekday, time_slots, module_code, cohort_id):
    total_slots = 0
    for record in schedule_list:
        if record["day"] == weekday and record["section"] == cohort_id and record["course"] == module_code:
            total_slots += len(record["periods"])

    if total_slots + len(time_slots) > 2:
        return False, f"Notice: High volume of {module_code} on {weekday}"
    return True, ""


def assess_preferences(schedule_list, weekday, time_slots, module_code, cohort_id):
    alerts = []

    ok, note = verify_daily_course_limit(schedule_list, weekday, module_code, cohort_id)
    if not ok: alerts.append(note)

    ok, note = verify_load_distribution(schedule_list, weekday, time_slots, module_code, cohort_id)
    if not ok: alerts.append(note)

    return alerts


# ==========================================
# ENTRY POINT
# ==========================================

def process_schedule_validation(schedule_list, weekday, time_slots, venue_obj, cohort_id, module_code, activity_cat,
                                credits_left, instructor_name=""):
    ok, msg = verify_workload_limit(time_slots, credits_left)
    if not ok: return False, f"Denied: {msg}", []

    ok, msg = verify_sequence_logic(time_slots, credits_left)
    if not ok: return False, f"Denied: {msg}", []

    ok, msg = verify_venue_suitability(activity_cat, venue_obj.room_type)
    if not ok: return False, f"Denied: {msg}", []

    ok, msg = verify_venue_availability(schedule_list, weekday, time_slots, venue_obj.room_no)
    if not ok: return False, f"Denied: {msg}", []

    ok, msg = verify_instructor_availability(schedule_list, weekday, time_slots, instructor_name)
    if not ok: return False, f"Denied: {msg}", []

    ok, msg = verify_batch_availability(schedule_list, weekday, time_slots, cohort_id)
    if not ok: return False, f"Denied: {msg}", []

    alerts = assess_preferences(schedule_list, weekday, time_slots, module_code, cohort_id)

    return True, "Valid assignment", alerts