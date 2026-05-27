from fastapi import FastAPI, HTTPException , Depends
from .service import HabitTracker
from pydantic import BaseModel
from .db import create_db_and_tables , get_session
from contextlib import asynccontextmanager
from sqlmodel import Session

@asynccontextmanager
async def lifespan(app:FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan = lifespan)

habits = HabitTracker()


class HabitCreated(BaseModel):
    habit: str
    category: str


class HabitEdit(BaseModel):
    new_habit: str | None = None
    new_category: str | None = None


@app.get("/habits")
def get_habits(session: Session = Depends(get_session)):
    return habits.get_all_habits(session)


@app.post("/habits")
def create_habit(data: HabitCreated , 
                 session: Session = Depends(get_session)
                 ):

    try:
        created_habit = habits.add_new_habit(
            habit=data.habit,
            category=data.category,
            session = session
        )

        return created_habit

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@app.patch("/habits/{habit_id}/complete")
def mark_habit_done(habit_id: str , session: Session = Depends(get_session)):
    try:
        updated_habit = habits.mark_habit_done(habit_id , session = session)

        return updated_habit

    except ValueError as e:

        if str(e) == "Habit ID not found":
            raise HTTPException(
                status_code=404,
                detail=str(e)
            )

        raise HTTPException(
            status_code=409,
            detail=str(e)
        )


@app.get("/habits/{habit_id}/streak")
def get_current_streak(habit_id: str , session: Session = Depends(get_session)):

    try:
        current_streak = habits.get_current_streak(habit_id , session)

        return {
            "current_streak": current_streak
        }

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@app.get("/habits/{habit_id}/max-streak")
def get_max_streak(habit_id: str , session: Session = Depends(get_session)):
    try:
        max_streak = habits.get_max_streak(habit_id , session)

        return {
            "max_streak": max_streak
        }

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@app.patch("/habits/{habit_id}")
def edit_habit(habit_id: str, data: HabitEdit , session: Session = Depends(get_session)):
    try:
        edited_habit = habits.edit_habit(
            habit_id,
            data.new_habit,
            data.new_category,
            session = session
        )

        return edited_habit

    except ValueError as e:

        if str(e) == "Habit ID not found":
            raise HTTPException(
                status_code=404,
                detail=str(e)
            )

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@app.delete("/habits/{habit_id}")
def delete_habit(habit_id: str , session: Session = Depends(get_session)):
    try:
        deleted_habit = habits.delete_habit(habit_id , session= session)

        return deleted_habit

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )