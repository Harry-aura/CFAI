import sys
import random
from project import DATA
from project.CONSTRAINS import process_schedule_validation

random.seed(42)

_total_attempts = 0
_total_assigned = 0
_total_rejected = 0


def _reset_counters():
    global _total_attempts, _total_assigned, _total_rejected
    _total_attempts, _total_assigned, _total_rejected = 0, 0, 0


def get_day_load(current_timetable, day, section_name):
    return sum(len(entry["periods"]) for entry in current_timetable if
               entry["day"] == day and entry["section"] == section_name)


def course_exists_same_day(current_timetable, day, course_alias, section_name):
    return any(entry["day"] == day and entry["section"] == section_name and entry["course"] == course_alias for entry in
               current_timetable)


def get_block_usage_count(current_timetable, periods, section_name):
    return sum(1 for entry in current_timetable if entry["periods"] == periods and entry["section"] == section_name)


def get_block_index(periods):
    if "P1" in periods or "P2" in periods: return 0
    if "P3" in periods or "P4" in periods: return 1
    if "P5" in periods or "P6" in periods: return 2
    if "P7" in periods or "P8" in periods: return 3
    return 99


def calculate_gap_score(current_timetable, day, periods, section_name):
    occupied_indices = [get_block_index(e["periods"]) for e in current_timetable if
                        e["day"] == day and e["section"] == section_name]
    target_idx = get_block_index(periods)
    if not occupied_indices: return 2 if target_idx >= 2 else 0
    return min(abs(target_idx - occ_idx) for occ_idx in occupied_indices)


def filter_rooms_by_class_type(class_type):
    if class_type == 'P': return [r for r in DATA.venue_inventory if r.room_type == 'Lab']
    return [r for r in DATA.venue_inventory if r.room_type == 'Theory']


def is_faculty_free(current_timetable, day, periods, faculty):
    if not faculty: return True
    for entry in current_timetable:
        if entry["day"] == day and entry.get("faculty") == faculty:
            if any(p in entry["periods"] for p in periods): return False
    return True


def is_section_free(current_timetable, day, periods, section_name):
    for entry in current_timetable:
        if entry["day"] == day and entry["section"] == section_name:
            if any(p in entry["periods"] for p in periods): return False
    return True


def is_room_free(current_timetable, day, periods, room_no):
    for entry in current_timetable:
        if entry["day"] == day and entry["room"] == room_no:
            if any(p in entry["periods"] for p in periods): return False
    return True


def get_course_scheduling_units(course):
    ltps_dict = {'L': course.hours[0], 'T': course.hours[1], 'P': course.hours[2], 'S': course.hours[3]}
    priority_order = {'P': 0, 'L': 1, 'S': 2, 'T': 3}
    units = [(ctype, count) for ctype, count in ltps_dict.items() if count > 0]
    units.sort(key=lambda x: (priority_order.get(x[0], 99), -x[1]))
    return units


def score_timetable(timetable_dict):
    score = 0.0
    for section_name, entries in timetable_dict.items():
        day_loads = [sum(len(e["periods"]) for e in entries if e["day"] == day) for day in DATA.week_calendar]
        if day_loads:
            avg_load = sum(day_loads) / len(day_loads)
            score += (sum((l - avg_load) ** 2 for l in day_loads) / len(day_loads)) * 10
        for day in DATA.week_calendar:
            day_entries = [e for e in entries if e["day"] == day]
            if not day_entries: continue
            occupied_blocks = sorted(set(get_block_index(e["periods"]) for e in day_entries))
            if len(occupied_blocks) >= 2:
                for b in range(occupied_blocks[0] + 1, occupied_blocks[-1]):
                    if b not in occupied_blocks: score += 5
            courses_on_day = [e["course"] for e in day_entries]
            score += (len(courses_on_day) - len(set(courses_on_day))) * 8
    return score


def _generate_timetable_attempt():
    global _total_attempts, _total_assigned, _total_rejected
    jarvis_protocol_schedule = []

    for section in DATA.batch_list:
        section_name = section.name
        sys.stdout.flush()

        sorted_courses = sorted(DATA.subject_registry, key=lambda c: (-c.hours[2], -c.weekly_load))

        for course in sorted_courses:
            units = get_course_scheduling_units(course)

            for class_type, total_periods_needed in units:
                remaining_classes = total_periods_needed
                valid_rooms = filter_rooms_by_class_type(class_type)

                while remaining_classes > 0:
                    assigned = False
                    periods_to_assign = 2 if remaining_classes >= 2 else 1
                    preferred_days, fallback_days = [], []

                    for day in DATA.week_calendar:
                        if course_exists_same_day(jarvis_protocol_schedule, day, course.alias, section_name):
                            fallback_days.append(day)
                        else:
                            preferred_days.append(day)

                    preferred_days.sort(key=lambda d: get_day_load(jarvis_protocol_schedule, d, section_name))
                    fallback_days.sort(key=lambda d: get_day_load(jarvis_protocol_schedule, d, section_name))
                    candidate_days = preferred_days + fallback_days

                    for day in candidate_days:
                        if assigned: break

                        blocks_to_try = [list(b) for b in DATA.consecutive_blocks] if periods_to_assign == 2 else [[p]
                                                                                                                   for p
                                                                                                                   in
                                                                                                                   DATA.slot_map.keys()]
                        blocks_to_try.sort(
                            key=lambda b: (calculate_gap_score(jarvis_protocol_schedule, day, b, section_name),
                                           get_block_usage_count(jarvis_protocol_schedule, b, section_name)))

                        for periods in blocks_to_try:
                            if assigned: break
                            if not is_section_free(jarvis_protocol_schedule, day, periods, section_name): continue
                            if not is_faculty_free(jarvis_protocol_schedule, day, periods, course.tutor): continue

                            available_rooms = [r for r in valid_rooms if
                                               is_room_free(jarvis_protocol_schedule, day, periods, r.room_no)]
                            available_rooms.sort(key=lambda r: r.room_no)

                            for room in available_rooms:
                                _total_attempts += 1
                                is_valid, msg, warnings = process_schedule_validation(
                                    jarvis_protocol_schedule, day, periods, room, section_name,
                                    course.alias, class_type, remaining_classes, instructor_id=course.tutor
                                )

                                if is_valid:
                                    jarvis_protocol_schedule.append({
                                        "day": day, "periods": periods, "room": room.room_no,
                                        "section": section_name, "course": course.alias,
                                        "faculty": course.tutor, "class_type": class_type
                                    })
                                    remaining_classes -= len(periods)
                                    assigned = True
                                    _total_assigned += 1
                                    break
                                else:
                                    _total_rejected += 1

                    if not assigned: return None

    timetable_dict = {section.name: [] for section in DATA.batch_list}
    for entry in jarvis_protocol_schedule:
        timetable_dict[entry["section"]].append(entry)

    return timetable_dict


def execute_scheduler():
    sys.stdout.flush()
    _reset_counters()
    random.seed(42)
    timetable_dict = _generate_timetable_attempt()
    if timetable_dict is not None:
        return timetable_dict
    sys.stdout.flush()
    return None