# Timetable Scheduling Technical Interview Defense

### Q1: Why is university timetabling classified as NP-hard?
> **Answer**: Academic scheduling can be reduced to the graph coloring problem (where vertices represent classes, edges represent conflicts such as shared teachers or students, and colors represent time slots). Graph k-coloring for k >= 3 is NP-complete.

### Q2: What heuristic is used to avoid deep recursive backtracking traps?
> **Answer**: MRV (Minimum Remaining Values), often called the "most constrained variable" heuristic, selects the class that has the fewest legal slot choices remaining, detecting failures as early as possible.

### Q3: How do you handle faculty preference weights without violating room capacity rules?
> **Answer**: Hard constraints are strict binary conditions (violation score = infinity). Soft constraints (such as faculty preferences) are evaluated via a normalized penalty function that only operates on schedules that have passed all hard checks.
