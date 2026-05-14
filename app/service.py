import uuid
from typing import Literal
from datetime import datetime, timedelta
from .models import Habit
from .validator import valid_habit, valid_category


class HabitTracker:

    def __init__(self):
        self.habits = {}

    def _get_habit(self, habit_id):
        try:
            return self.habits[habit_id]
        except KeyError:
            raise ValueError("Habit ID not found")

    def add_new_habit(self, habit, category: Literal['Health', 'Productivity', 'Personal', 'Social', 'Other']):
        habit_id = str(uuid.uuid4())
        habit = valid_habit(habit)
        category = valid_category(category)

        habit_obj = Habit(
            habit_id=habit_id,
            habit=habit,
            category=category,
            created_at=datetime.now()
        )

        self.habits[habit_id] = habit_obj
        return habit_obj

    def mark_habit_done(self, habit_id):
        habit = self._get_habit(habit_id)

        today = datetime.now().date()

        if today in habit.completed_days:
            raise ValueError("Habit already marked completed")

        habit.completed_days.add(today)
        return habit

    def get_current_streak(self, habit_id):
        habit = self._get_habit(habit_id)

        today = datetime.now().date()
        yesterday = today - timedelta(days=1)

        if today in habit.completed_days:
            current = today
        elif yesterday in habit.completed_days:
            current = yesterday
        else:
            return 0

        streak = 0

        while current in habit.completed_days:
            streak += 1
            current -= timedelta(days=1)

        return streak

    def get_max_streak(self, habit_id):
        habit = self._get_habit(habit_id)
        
        days = habit.completed_days
        
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

    def edit_habit(self, habit_id, new_habit=None, new_category=None):
        habit = self._get_habit(habit_id)

        
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

        return habit

    def delete_habit(self, habit_id):
        habit = self._get_habit(habit_id)

        return self.habits.pop(habit_id)
    
    def get_all_habits(self):
        return sorted(self.habits.values(), key=lambda h: h.created_at)
    
    def get_habit_by_id(self , habit_id):
        habit = self._get_habit(habit_id)
        return habit
        
    