from MODULES import Subject, Venue, Batch

# Actual Semester Courses
# Mapping your 'Course' to our 'Subject' class
subject_registry = [
    Subject(code="25MT1306E", name="MATHEMATICS FOR DATA SCIENCE AND ANALYTICS", alias="MDSA", hours=(2, 0, 4, 0), tutor="Dr Rao"),
    Subject(code="25SC1305E", name="DATA STRUCTURES AND ALGORITHMS - 2", alias="DSA2", hours=(4, 0, 2, 4), tutor="Dr Sharma"),
    Subject(code="25SC1306E", name="COMPUTATIONAL FOUNDATIONS FOR ARTIFICIAL INTELLIGENCE", alias="CFAI", hours=(4, 0, 0, 4), tutor="Dr Kumar"),
    Subject(code="25CS1201E", name="FRONT END DEVELOPMENT FRAMEWORKS AND UI ENGINEERING", alias="FEDF", hours=(0, 0, 4, 4), tutor="Dr Priya"),
    Subject(code="25FL1301E", name="GERMAN LANGUAGE PROFICIENCY", alias="FL", hours=(0, 0, 4, 0), tutor="Dr Ramesh"),
    Subject(code="25UC0036", name="GLOBAL LOGIC BUILDING CONTEST PRACTICUM", alias="GLB", hours=(0, 0, 0, 4), tutor="Dr Anitha")
]

# Theory + Lab Rooms
venue_inventory = [
    Venue(room_no="101", room_type="Theory"), Venue(room_no="102", room_type="Theory"),
    Venue(room_no="103", room_type="Theory"), Venue(room_no="104", room_type="Theory"),
    Venue(room_no="L1", room_type="Lab"), Venue(room_no="L2", room_type="Lab"),
    Venue(room_no="L3", room_type="Lab"), Venue(room_no="L4", room_type="Lab")
]

# Sections mapped to Batch class
batch_list = [Batch(name="1"), Batch(name="2"), Batch(name="3"), Batch(name="4")]

# Days and Periods
week_calendar = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

slot_map = {
    "P1": "8:10–9:00", "P2": "9:00–9:50",
    "P3": "10:00–10:50", "P4": "10:50–11:40",
    "P5": "12:20–1:10", "P6": "1:10–2:00",
    "P7": "2:10–3:00", "P8": "3:00–3:50"
}

consecutive_blocks = [("P1", "P2"), ("P3", "P4"), ("P5", "P6"), ("P7", "P8")]