# Algorithmic Complexity & Scalability Design

## 1. The NP-Hard Timetabling Challenge
Determining whether a timetable exists without hard constraint violations in an unconstrained search space is NP-complete. A naive brute-force permutation search produces factorial time complexity O(D^V).

## 2. Heuristic Pruning Guarantees
- Forward checking prunes domains before assignment failures cascade.
- Constraint propagation guarantees that impossible assignments are rejected early in the search tree, keeping runtime under 2 seconds for full department matrices.
