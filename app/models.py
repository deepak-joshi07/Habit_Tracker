from dataclasses import dataclass , field
from typing import Set, Optional
from datetime import datetime , date
@dataclass
class Habit:
    habit_id : str
    habit : str
    category : str
    created_at : datetime
    completed_days: Set[date] = field(default_factory=set)
    updated_at: Optional[datetime] = None

        