from dataclasses import dataclass

@dataclass
class Subject:
    code: str
    name: str
    alias: str
    hours: tuple[int, int, int, int]
    tutor: str = ""
    @property
    def weekly_load(self) -> int: return sum(self.hours)

@dataclass
class Venue:
    room_no: str
    room_type: str

@dataclass
class Batch:
    name: str
