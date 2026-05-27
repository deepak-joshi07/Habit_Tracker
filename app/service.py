import uuid
from typing import Literal
from datetime import datetime, timedelta
from .models import Habit , HabitCompletion
from .validator import valid_habit, valid_category
from sqlmodel import select , Session


class HabitTracker:

    def _get_habit(self, habit_id , session):
        habit = session.exec(select(Habit).where(Habit.habit_id == habit_id)).first()

        if not habit:
            raise ValueError("Habit ID not found")
        
        return habit
    
    def add_new_habit(self, habit, category: Literal['Health', 'Productivity', 'Personal', 'Social', 'Other'] , session):
        habit_id = str(uuid.uuid4())
        habit = valid_habit(habit)
        category = valid_category(category)

        habit_obj = Habit(
            habit_id=habit_id,
            habit=habit,
            category=category,
            created_at=datetime.now()
        )

        session.add(habit_obj)
        session.commit()
        session.refresh(habit_obj)
        return habit_obj

    def mark_habit_done(self, habit_id , session):
        self._get_habit(habit_id , session)

        today = datetime.now().date()

        existing_completion = session.exec(
            select(HabitCompletion).where(
                HabitCompletion.habit_id == habit_id,
                HabitCompletion.completed_date == today
            )
        ).first()

        if existing_completion:
            raise ValueError("Habit already marked completed")

        completion = HabitCompletion(habit_id = habit_id, completed_date= today)
        session.add(completion)
        session.commit()
        session.refresh(completion)
        return completion

    def get_current_streak(self, habit_id , session):
        self._get_habit(habit_id, session)
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)

        completion_today = session.exec(
            select(HabitCompletion).where(
                HabitCompletion.habit_id == habit_id,
                HabitCompletion.completed_date == today
            )
        ).first()

        completion_yesterday = session.exec(
            select(HabitCompletion).where(
                HabitCompletion.habit_id == habit_id , 
                HabitCompletion.completed_date == yesterday
            )
        ).first()

        if completion_today:
            current = today
        elif completion_yesterday:
            current = yesterday
        else:
            return 0

        streak = 0

        completion = session.exec(
            select(HabitCompletion.completed_date)
            .where(HabitCompletion.habit_id == habit_id)
        ).all()

        completed_days = set(completion)

        while current in completed_days:
            streak += 1
            current -= timedelta(days=1)

        return streak

    def get_max_streak(self, habit_id , session):
        self._get_habit(habit_id, session)
        days = session.exec(
            select(HabitCompletion.completed_date)
            .where(HabitCompletion.habit_id == habit_id)
        ).all()
        
        if not days:
            return 0

        dates = sorted(days)

        max_streak = 1
        current_streak = 1

        for i in range(1, len(dates)):
            if dates[i] == dates[i - 1] + timedelta(days=1):
                current_streak += 1
            else:
                current_streak = 1

            max_streak = max(max_streak, current_streak)

        return max_streak

    def edit_habit(self, habit_id, new_habit=None, new_category=None , session: Session = None):
        habit = self._get_habit(habit_id , session)

        
        updated = False

        if new_habit is None and new_category is None:
            raise ValueError("At least one field must be provided")

        if new_habit:
            validated = valid_habit(new_habit)
            if validated != habit.habit:
                habit.habit = validated
                updated = True

        if new_category:
            validated = valid_category(new_category)
            if validated != habit.category:
                habit.category = validated
                updated = True

        if updated:
            habit.updated_at = datetime.now()
            session.commit()
            session.refresh(habit)

        return habit

    def delete_habit(self, habit_id , session):
        habit = self._get_habit(habit_id , session)
        session.delete(habit)
        session.commit()
        return habit
    
    def get_all_habits(self , session):
        return session.exec(select(Habit)).all()
    
    def get_habit_by_id(self , habit_id , session):
        habit = self._get_habit(habit_id , session)
        return habit
        
    