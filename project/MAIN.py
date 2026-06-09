from dataclasses import dataclass

@dataclass
class Subject:
    id_code: str
    full_title: str
    abbreviation: str
    load_structure: tuple[int, int, int, int]  # (Lecture, Tutorial, Practical, Skill)
    instructor: str = ""

    @property
    def weekly_load(self) -> int:
        """Calculate aggregate weekly sessions from the load structure."""
        return sum(self.load_structure)

@dataclass
class Facility:
    identifier: str
    category: str  # e.g., 'Theory' or 'Lab'

@dataclass
class Cohort:
    label: str