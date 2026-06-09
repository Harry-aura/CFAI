from project import DATA, schedular


def render_table(schedules):
    for cohort, records in schedules.items():
        # Print a clear header for each section
        print("\n" + "=" * 120)
        print(f" TIMETABLE FOR SECTION: {cohort} ".center(120, "="))
        print("=" * 120)

        # Print column headers (P1, P2, etc.)
        header = f"{'Day':<12}"
        for slot in DATA.slot_map.keys():
            header += f"| {slot:<12}"
        print(header)
        print("-" * 120)

        # Print the schedule for each day
        for day in DATA.week_calendar:
            row_str = f"{day:<12}"
            for slot in DATA.slot_map.keys():
                found = "FREE"
                for r in records:
                    if r['day'] == day and slot in r['periods']:
                        found = f"{r['course']}-{r['room']}"
                        break
                row_str += f"| {found:<12}"
            print(row_str)

        print("=" * 120 + "\n")


if __name__ == "__main__":
    print("Generating Timetable...")
    data = schedular.execute_scheduler()

    if data:
        render_table(data)
    else:
        print("Failed to generate. Constraints might be too tight.")