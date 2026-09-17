# Timetable Generation Data Flow & Conflict Resolution

~~~text
[Faculty, Course & Room Constraints Loaded]
                     │
                     ▼
         [Build Conflict Graph]
                     │
                     ▼
   [Variable Ordering via MRV Heuristic]
                     │
                     ▼
     [Forward Checking Slot Allocation]
                     │
           {Hard Conflict Detected?}
           ├── Yes ──> [Backtrack to Prior Assignment State]
           └── No ───> [Commit Slot & Evaluate Soft Objective Score]
                     │
                     ▼
     [Emit Structured Master Schedule Matrix]
~~~
