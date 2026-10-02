from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class PeriodSlot:
    id: int
    label: str
    start_time: object
    end_time: object


@dataclass
class TeacherConstraintData:
    teacher_id: int
    type: str  # 'unavailable' | 'max_consecutive_lessons'
    parameters: dict


@dataclass
class TeachingUnit:
    """One subject's weekly requirement for one owner (a stream, or one option group)."""
    unit_id: str
    teacher_id: int
    subject_id: int
    owner_type: str   # 'stream' or 'option_group'
    owner_id: int
    lessons_per_week: int
    doubles_per_week: int
    max_lessons_per_day: Optional[int]
    resource_id: Optional[int]


@dataclass
class OptionBlockGroup:
    """Units that must always land on the same slot, because they're the same elective split."""
    block_id: int
    unit_ids: List[str]


@dataclass
class SolverInput:
    school_id: str
    term_id: int
    days: List[str]
    periods: List[PeriodSlot]                       # teaching periods only, ordered by start_time
    double_adjacent_pairs: List[tuple]                # (period_id_a, period_id_b) — valid double slots
    units: List[TeachingUnit]
    option_blocks: List[OptionBlockGroup]
    teacher_constraints: List[TeacherConstraintData]
    resource_capacity: dict                           # resource_id -> capacity


@dataclass
class PlacedLesson:
    unit_id: str
    day: str
    period_id: int
    double_group_id: Optional[int] = None