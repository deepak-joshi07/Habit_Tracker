from sqlmodel import SQLModel , Field
from typing import Optional
from datetime import datetime , date

class Habit(SQLModel, table=True):
    habit_id : str = Field(primary_key= True)
    habit : str = Field(index = True)
    category : str
    created_at : datetime
    updated_at: Optional[datetime] = Field(default=None)

class HabitCompletion(SQLModel , table = True):
    id: int | None = Field(default=None, primary_key=True)
    habit_id: str = Field(foreign_key="habit.habit_id") 
    completed_date : date 


        