from project import DATA
from collections import defaultdict


def consolidate_schedule(total_schedules):
    """
    Transforms the cohort-grouped schedule dict into a unified list
    for global constraint audits.
    """
    master_list = []
    for cohort_id, records in total_schedules.items():
        master_list.extend(records)
    return master_list


def verify_no_venue_conflict(total_schedules):
    """
    Checks for global venue clashes (two groups in one room, same time).
    """
    master_list = consolidate_schedule(total_schedules)
    status_ok = True

    venue_map = defaultdict(list)
    for record in master_list:
        venue_map[(record["day"], record["room"])].append(record)

    for (day, venue), items in venue_map.items():
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                r1, r2 = items[i], items[j]

                intersect = set(r1["periods"]).intersection(r2["periods"])
                if intersect:
                    overlap_id = "-".join(sorted(list(intersect)))
                    print("VENUE CONFLICT DETECTED:")
                    print(f"{day} | {overlap_id} | Venue {venue}")
                    print(f"Groups: {r1['section']} and {r2['section']}\n")
                    status_ok = False

    return status_ok


def verify_no_tutor_conflict(total_schedules):
    """
    Checks for global tutor clashes (one tutor assigned to two groups, same time).
    """
    master_list = consolidate_schedule(total_schedules)
    status_ok = True

    tutor_map = defaultdict(list)
    for record in master_list:
        tutor = record.get("faculty")
        if tutor:
            tutor_map[(record["day"], tutor)].append(record)

    for (day, tutor), items in tutor_map.items():
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                r1, r2 = items[i], items[j]

                intersect = set(r1["periods"]).intersection(r2["periods"])
                if intersect:
                    overlap_id = "-".join(sorted(list(intersect)))
                    print("TUTOR CONFLICT DETECTED:")
                    print(f"{tutor} | {day} | {overlap_id}")
                    print(f"Group {r1['section']} -> {r1['course']}")
                    print(f"Group {r2['section']} -> {r2['course']}\n")
                    status_ok = False

    return status_ok


def verify_no_batch_conflict(total_schedules):
    """
    Ensures a single group never has two simultaneous sessions.
    """
    status_ok = True

    for cohort_id, records in total_schedules.items():
        day_map = defaultdict(list)
        for record in records:
            day_map[record["day"]].append(record)

        for day, daily_records in day_map.items():
            for i in range(len(daily_records)):
                for j in range(i + 1, len(daily_records)):
                    r1, r2 = daily_records[i], daily_records[j]

                    intersect = set(r1["periods"]).intersection(r2["periods"])
                    if intersect:
                        overlap_id = "-".join(sorted(list(intersect)))
                        print("BATCH CONFLICT DETECTED:")
                        print(f"Batch {cohort_id}")
                        print(f"{day} | {overlap_id} | {r1['course']} vs {r2['course']}\n")
                        status_ok = False

    return status_ok


def verify_credit_hours(total_schedules):
    """
    Confirms total allocated hours match course requirements.
    """
    status_ok = True

    req_lookup = {}
    for mod in DATA.subject_registry:
        req_lookup[mod.alias] = {
            'L': mod.hours[0],
            'T': mod.hours[1],
            'P': mod.hours[2],
            'S': mod.hours[3]
        }

    for cohort_id, records in total_schedules.items():
        alloc_found = defaultdict(lambda: defaultdict(int))
        for record in records:
            mod = record["course"]
            m_type = record["class_type"]
            alloc_found[mod][m_type] += len(record["periods"])

        for mod_alias in req_lookup:
            for m_type in ['L', 'T', 'P', 'S']:
                needed = req_lookup[mod_alias][m_type]
                active = alloc_found[mod_alias][m_type]

                if needed != active:
                    print(f"CREDIT LOAD MISMATCH: Batch {cohort_id} | {mod_alias} ({m_type})")
                    print(f"Needed: {needed} | Found: {active}\n")
                    status_ok = False

    return status_ok


def verify_spatial_mode(total_schedules):
    """
    Ensures 'P' modes are in Labs, all others in Theory rooms.
    """
    status_ok = True
    venue_cat_map = {v.room_no: v.room_type for v in DATA.venue_inventory}

    master_list = consolidate_schedule(total_schedules)
    for record in master_list:
        v_cat = venue_cat_map[record["room"]]
        m_type = record["class_type"]

        if m_type == 'P' and v_cat != 'Lab':
            print(f"SPATIAL MISMATCH: {record['section']} | {record['course']} ({m_type}) in {record['room']} (Theory)")
            status_ok = False
        elif m_type in ['L', 'T', 'S'] and v_cat != 'Theory':
            print(f"SPATIAL MISMATCH: {record['section']} | {record['course']} ({m_type}) in {record['room']} (Lab)")
            status_ok = False

    return status_ok


def run_integrity_audit(total_schedules):
    """
    Executes full suite of tests.
    """
    print("\n" + "=" * 40)
    print("GLOBAL INTEGRITY AUDIT")
    print("=" * 40 + "\n")

    t1 = verify_no_venue_conflict(total_schedules)
    t2 = verify_no_batch_conflict(total_schedules)
    t3 = verify_credit_hours(total_schedules)
    t4 = verify_spatial_mode(total_schedules)
    t5 = verify_no_tutor_conflict(total_schedules)

    print("-" * 40)
    print(f"Venue Check:   {'OK' if t1 else 'FAILED'}")
    print(f"Batch Check:   {'OK' if t2 else 'FAILED'}")
    print(f"Tutor Check:   {'OK' if t5 else 'FAILED'}")
    print(f"Credit Check:  {'OK' if t3 else 'FAILED'}")
    print(f"Spatial Check: {'OK' if t4 else 'FAILED'}")
    print("-" * 40)

    if all([t1, t2, t3, t4, t5]):
        print("\nINTEGRITY AUDIT PASSED\n")
        return True
    else:
        print("\nINTEGRITY AUDIT FOUND FAILURES\n")
        return False